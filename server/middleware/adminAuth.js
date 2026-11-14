const { findAdminById } = require('../auth');

async function requireAdmin(req, res, next) {
  try {
    const adminId = req.session?.adminId;

    if (!adminId) {
      return res.status(401).json({ error: 'Autenticação necessária.' });
    }

    const admin = await findAdminById(adminId);

    if (!admin) {
      if (req.session) {
        req.session.destroy(() => {});
      }

      return res.status(401).json({ error: 'Sessão inválida.' });
    }

    req.admin = admin;
    next();
  } catch (error) {
    next(error);
  }
}

function requireRole(...allowedRoles) {
  return (req, res, next) => {
    if (!req.admin) {
      return res.status(401).json({ error: 'Autenticação necessária.' });
    }

    if (!allowedRoles.includes(req.admin.role)) {
      return res.status(403).json({ error: 'Permissão insuficiente.' });
    }

    next();
  };
}

module.exports = {
  requireAdmin,
  requireRole
};
