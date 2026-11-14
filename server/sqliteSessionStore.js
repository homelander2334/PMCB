const session = require("express-session");

class SQLiteSessionStore extends session.Store {
  constructor(db) {
    super();
    this.db = db;

    this.getStatement = db.prepare(
      "SELECT sess, expired FROM sessions WHERE sid = ?"
    );

    this.setStatement = db.prepare(
      "INSERT INTO sessions (sid, sess, expired) VALUES (?, ?, ?) " +
      "ON CONFLICT(sid) DO UPDATE SET sess = excluded.sess, expired = excluded.expired"
    );

    this.destroyStatement = db.prepare(
      "DELETE FROM sessions WHERE sid = ?"
    );

    this.touchStatement = db.prepare(
      "UPDATE sessions SET expired = ? WHERE sid = ?"
    );

    this.cleanupStatement = db.prepare(
      "DELETE FROM sessions WHERE expired <= ?"
    );
  }

  get(sid, callback) {
    try {
      const row = this.getStatement.get(sid);

      if (!row) return callback(null, null);

      if (row.expired <= Date.now()) {
        this.destroyStatement.run(sid);
        return callback(null, null);
      }

      callback(null, JSON.parse(row.sess));
    } catch (error) {
      callback(error);
    }
  }

  set(sid, sess, callback = () => {}) {
    try {
      const expires = sess.cookie && sess.cookie.expires
        ? new Date(sess.cookie.expires).getTime()
        : Date.now() + (
            sess.cookie && sess.cookie.maxAge
              ? sess.cookie.maxAge
              : 86400000
          );

      this.setStatement.run(sid, JSON.stringify(sess), expires);
      callback(null);
    } catch (error) {
      callback(error);
    }
  }

  destroy(sid, callback = () => {}) {
    try {
      this.destroyStatement.run(sid);
      callback(null);
    } catch (error) {
      callback(error);
    }
  }

  touch(sid, sess, callback = () => {}) {
    try {
      const expires = sess.cookie && sess.cookie.expires
        ? new Date(sess.cookie.expires).getTime()
        : Date.now() + (
            sess.cookie && sess.cookie.maxAge
              ? sess.cookie.maxAge
              : 86400000
          );

      this.touchStatement.run(expires, sid);
      callback(null);
    } catch (error) {
      callback(error);
    }
  }

  cleanup() {
    this.cleanupStatement.run(Date.now());
  }
}

module.exports = SQLiteSessionStore;
