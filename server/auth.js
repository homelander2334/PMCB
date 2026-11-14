const bcrypt = require('bcryptjs');
const db = require('./database');

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

async function createAdmin({ name, email, password, role = 'editor' }) {
  if (typeof name !== 'string' || name.trim().length < 2) {
    throw new Error('Nome inválido.');
  }

  if (!['superadmin', 'admin', 'editor'].includes(role)) {
    throw new Error('Função administrativa inválida.');
  }

  const normalizedEmail = normalizeEmail(email);
  const passwordHash = await hashPassword(password);

  const result = db.prepare(`
    INSERT INTO admin_users (name, email, password_hash, role)
    VALUES (?, ?, ?, ?)
  `).run(name.trim(), normalizedEmail, passwordHash, role);

  return Number(result.lastInsertRowid);
}

async function authenticateAdmin(email, password) {
  const normalizedEmail = normalizeEmail(email);

  const user = db.prepare(`
    SELECT id, name, email, password_hash, role, active
    FROM admin_users
    WHERE email = ?
    LIMIT 1
  `).get(normalizedEmail);

  if (!user || user.active !== 1) {
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
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role
  };
}

function findAdminById(id) {
  const user = db.prepare(`
    SELECT id, name, email, role, active
    FROM admin_users
    WHERE id = ?
    LIMIT 1
  `).get(id);

  if (!user || user.active !== 1) {
    return null;
  }

  return {
    id: user.id,
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
