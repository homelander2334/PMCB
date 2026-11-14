const { csrfSync } = require('csrf-sync');

const csrf = csrfSync({
  getTokenFromRequest: (req) =>
    req.headers['x-csrf-token'] || req.body?._csrf
});

module.exports = {
  generateToken: csrf.generateToken,
  invalidCsrfTokenError: csrf.invalidCsrfTokenError,
  csrfProtection: csrf.csrfSynchronisedProtection
};
