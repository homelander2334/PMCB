if (require('node:fs').existsSync('.env')) {
  process.loadEnvFile('.env');
}

const express = require('express');
const session = require('express-session');
const path = require('node:path');

const { db, initializeDatabase } = require('./database.pg');
const PostgresSessionStore = require('./postgresSessionStore');
const {
  authenticateAdmin,
  findAdminById
} = require('./auth');

const {
  securityHeaders,
  generalLimiter,
  loginLimiter,
  formLimiter
} = require('./middleware/security');

const {
  generateToken,
  csrfProtection,
  invalidCsrfTokenError
} = require('./middleware/csrf');

if (!process.env.SESSION_SECRET || process.env.SESSION_SECRET.length < 64) {
  throw new Error('SESSION_SECRET ausente ou inválida.');
}

const app = express();
const isProduction = process.env.NODE_ENV === 'production';

app.disable('x-powered-by');
app.set('trust proxy', process.env.TRUST_PROXY === '1' ? 1 : false);

app.use(securityHeaders);
app.use(generalLimiter);
app.use(express.json({ limit: '20kb' }));
app.use(express.urlencoded({ extended: false, limit: '20kb' }));

app.use(session({
  name: 'pmcb.sid',
  secret: process.env.SESSION_SECRET,
  store: new PostgresSessionStore(db),
  resave: false,
  saveUninitialized: false,
  rolling: true,
  cookie: {
    httpOnly: true,
    secure: isProduction,
    sameSite: 'strict',
    maxAge: 8 * 60 * 60 * 1000,
    path: '/'
  }
}));

app.use(csrfProtection);

app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    service: 'PMCB',
    status: 'online'
  });
});

app.get('/api/csrf', (req, res) => {
  res.json({
    success: true,
    csrfToken: generateToken(req)
  });
});

app.post('/api/admin/login', loginLimiter, async (req, res, next) => {
  try {
    const { email, password } = req.body || {};

    if (typeof email !== 'string' || typeof password !== 'string') {
      return res.status(400).json({
        success: false,
        message: 'Informe e-mail e senha.'
      });
    }

    const admin = await authenticateAdmin(email, password);

    if (!admin) {
      return res.status(401).json({
        success: false,
        message: 'Credenciais inválidas.'
      });
    }

    req.session.regenerate((error) => {
      if (error) return next(error);

      req.session.adminId = admin.id;

      const csrfToken = generateToken(req);

      req.session.save((saveError) => {
        if (saveError) return next(saveError);

        res.json({
          success: true,
          admin,
          csrfToken
        });
      });
    });
  } catch (error) {
    if (error.message === 'E-mail inválido.') {
      return res.status(400).json({
        success: false,
        message: 'E-mail inválido.'
      });
    }

    next(error);
  }
});

app.get('/api/admin/me', async (req, res, next) => {
  try {
    if (!req.session.adminId) {
      return res.status(401).json({
        success: false,
        message: 'Não autenticado.'
      });
    }

    const admin = await findAdminById(req.session.adminId);

    if (!admin) {
      return req.session.destroy(() => {
        res.status(401).json({
          success: false,
          message: 'Sessão inválida.'
        });
      });
    }

    res.json({ success: true, admin });
  } catch (error) {
    next(error);
  }
});

app.post('/api/admin/logout', (req, res) => {
  req.session.destroy((error) => {
    if (error) {
      return res.status(500).json({
        success: false,
        message: 'Não foi possível encerrar a sessão.'
      });
    }

    res.clearCookie('pmcb.sid', {
      httpOnly: true,
      secure: isProduction,
      sameSite: 'strict',
      path: '/'
    });

    res.json({
      success: true,
      message: 'Sessão encerrada.'
    });
  });
});

function readFormText(value, maxLength, required = false) {
  if (typeof value !== 'string') return required ? null : '';

  const text = value.trim();

  if (required && !text) return null;
  if (text.length > maxLength) return null;

  return text;
}

function validEmail(value) {
  return typeof value === 'string' &&
    value.length <= 254 &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

function hasPrivacyConsent(value) {
  return value === true ||
    value === 'true' ||
    value === '1' ||
    value === 'on';
}

app.post('/api/applications/supporter', formLimiter, async (req, res) => {
  const body = req.body || {};

  const name = readFormText(body.name, 120, true);
  const email = body.email;
  const phone = readFormText(body.phone, 30);
  const state = readFormText(body.state, 80);
  const city = readFormText(body.city, 100);
  const interests = readFormText(body.interests, 1000);

  if (
    !name ||
    !validEmail(email) ||
    phone === null ||
    state === null ||
    city === null ||
    interests === null ||
    !hasPrivacyConsent(body.privacy_consent)
  ) {
    return res.status(400).json({
      success: false,
      message: 'Confira os campos e autorize o tratamento dos dados.'
    });
  }

  try {
    const result = await db.query(
      `INSERT INTO supporter_applications
        (name, email, phone, state, city, interests, privacy_consent)
       VALUES ($1, $2, $3, $4, $5, $6, 1)
       RETURNING id`,
      [
        name,
        email.trim().toLowerCase(),
        phone,
        state,
        city,
        interests
      ]
    );

    return res.status(201).json({
      success: true,
      message: 'Interesse registrado para análise.',
      applicationId: Number(result.rows[0].id)
    });
  } catch (error) {
    console.error('Erro ao registrar apoiador:', error.message);

    return res.status(500).json({
      success: false,
      message: 'Não foi possível registrar o interesse.'
    });
  }
});

app.post('/api/applications/representative', formLimiter, async (req, res) => {
  const body = req.body || {};

  const name = readFormText(body.name, 120, true);
  const email = body.email;
  const phone = readFormText(body.phone, 30);
  const state = readFormText(body.state, 80, true);
  const city = readFormText(body.city, 100);
  const desiredPosition = readFormText(body.desired_position, 120);
  const experience = readFormText(body.experience, 1500);

  if (
    !name ||
    !validEmail(email) ||
    phone === null ||
    !state ||
    city === null ||
    desiredPosition === null ||
    experience === null ||
    !hasPrivacyConsent(body.privacy_consent)
  ) {
    return res.status(400).json({
      success: false,
      message: 'Confira os campos e autorize o tratamento dos dados.'
    });
  }

  try {
    const result = await db.query(
      `INSERT INTO representative_applications
        (name, email, phone, state, city, desired_position,
         experience, privacy_consent)
       VALUES ($1, $2, $3, $4, $5, $6, $7, 1)
       RETURNING id`,
      [
        name,
        email.trim().toLowerCase(),
        phone,
        state,
        city,
        desiredPosition,
        experience
      ]
    );

    return res.status(201).json({
      success: true,
      message: 'Interesse registrado para análise. Não representa nomeação oficial.',
      applicationId: Number(result.rows[0].id)
    });
  } catch (error) {
    console.error('Erro ao registrar representante:', error.message);

    return res.status(500).json({
      success: false,
      message: 'Não foi possível registrar o interesse.'
    });
  }
});

app.use(express.static(path.join(__dirname, '..', 'public')));

app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Rota não encontrada.'
  });
});

app.use((error, req, res, next) => {
  if (res.headersSent) return next(error);

  if (error === invalidCsrfTokenError) {
    return res.status(403).json({
      success: false,
      message: 'Token CSRF inválido ou ausente.'
    });
  }

  console.error('Erro interno:', error.message);

  res.status(500).json({
    success: false,
    message: 'Erro interno do servidor.'
  });
});

const PORT = Number(process.env.PORT) || 3000;

if (require.main === module) {
  initializeDatabase()
    .then(() => {
      app.listen(PORT, '0.0.0.0', () => {
        console.log('Portal PMCB iniciado na porta ' + PORT);
      });
    })
    .catch((error) => {
      console.error('Falha ao inicializar o banco:', error.message);
      process.exit(1);
    });
}

module.exports = app;
