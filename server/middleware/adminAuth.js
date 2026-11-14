const { findAdminById } = require('../auth');

function requireAdmin(req, res, next) {
  const adminId = req.session?.adminId;

  if (!adminId) {
    return res.status(401).json({
      success: false,
      message: 'Autenticação necessária.'
    });
  }

  const admin = findAdminById(adminId);

  if (!admin) {
    req.session.destroy(() => {});
    return res.status(401).json({
      success: false,
      message: 'Sessão inválida ou usuário desativado.'
    });
  }

  req.admin = admin;
  next();
}

function requireRole(...allowedRoles) {
  return (req, res, next) => {
    if (!req.admin) {
      return res.status(401).json({
        success: false,
        message: 'Autenticação necessária.'
      });
    }

    if (!allowedRoles.includes(req.admin.role)) {
      return res.status(403).json({
        success: false,
        message: 'Você não tem permissão para esta operação.'
      });
    }

    next();
  };
}

module.exports = {
  requireAdmin,
  requireRole
};
