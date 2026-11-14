const bcrypt = require('bcryptjs');
const { db } = require('./database.pg');

const SALT_ROUNDS = 12;

async function hashPassword(password) {
  if (typeof password !== 'string' || password.length < 12) {
    throw new Error('A senha deve ter pelo menos 12 caracteres.');
  }

  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password, passwordHash) {
  if (typeof password !== 'string' || typeof passwordHash !== 'string') {
    return false;
  }

  return bcrypt.compare(password, passwordHash);
}

function normalizeEmail(email) {
  if (typeof email !== 'string') {
    throw new Error('E-mail inválido.');
  }

  const normalized = email.trim().toLowerCase();

  if (
    normalized.length > 254 ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalized)
  ) {
    throw new Error('E-mail inválido.');
  }

  return normalized;
}

async function createAdmin({
  name,
  email,
  password,
  role = 'editor'
}) {
  if (typeof name !== 'string' || name.trim().length < 2) {
    throw new Error('Nome inválido.');
  }

  if (!['superadmin', 'admin', 'editor'].includes(role)) {
    throw new Error('Função inválida.');
  }

  const normalizedEmail = normalizeEmail(email);
  const passwordHash = await hashPassword(password);

  const result = await db.query(
    `INSERT INTO admin_users (name, email, password_hash, role)
     VALUES ($1, $2, $3, $4)
     RETURNING id`,
    [name.trim(), normalizedEmail, passwordHash, role]
  );

  return Number(result.rows[0].id);
}

async function authenticateAdmin(email, password) {
  let normalizedEmail;

  try {
    normalizedEmail = normalizeEmail(email);
  } catch {
    return null;
  }

  const result = await db.query(
    `SELECT id, name, email, password_hash, role, active
     FROM admin_users
     WHERE email = $1
     LIMIT 1`,
    [normalizedEmail]
  );

  const user = result.rows[0];

  if (!user || Number(user.active) !== 1) {
    return null;
  }

  const validPassword = await verifyPassword(
    password,
    user.password_hash
  );

  if (!validPassword) {
    return null;
  }

  return {
    id: Number(user.id),
    name: user.name,
    email: user.email,
    role: user.role
  };
}

async function findAdminById(id) {
  const result = await db.query(
    `SELECT id, name, email, role, active
     FROM admin_users
     WHERE id = $1
     LIMIT 1`,
    [id]
  );

  const user = result.rows[0];

  if (!user || Number(user.active) !== 1) {
    return null;
  }

  return {
    id: Number(user.id),
    name: user.name,
    email: user.email,
    role: user.role
  };
}

module.exports = {
  hashPassword,
  verifyPassword,
  normalizeEmail,
  createAdmin,
  authenticateAdmin,
  findAdminById
};
