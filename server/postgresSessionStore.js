const session = require('express-session');

class PostgresSessionStore extends session.Store {
  constructor(pool) {
    super();
    this.pool = pool;
  }

  get(sid, callback) {
    this.pool.query(
      'SELECT sess, expired FROM sessions WHERE sid = $1',
      [sid]
    ).then(async result => {
      if (!result.rows.length) {
        return callback(null, null);
      }

      const row = result.rows[0];

      if (Number(row.expired) <= Date.now()) {
        await this.pool.query(
          'DELETE FROM sessions WHERE sid = $1',
          [sid]
        );
        return callback(null, null);
      }

      callback(null, row.sess);
    }).catch(callback);
  }

  set(sid, sess, callback = () => {}) {
    const expired = sess.cookie?.expires
      ? new Date(sess.cookie.expires).getTime()
      : Date.now() + 8 * 60 * 60 * 1000;

    this.pool.query(
      `INSERT INTO sessions (sid, sess, expired)
       VALUES ($1, $2, $3)
       ON CONFLICT (sid)
       DO UPDATE SET sess = EXCLUDED.sess,
                     expired = EXCLUDED.expired`,
      [sid, JSON.stringify(sess), expired]
    ).then(() => callback(null)).catch(callback);
  }

  destroy(sid, callback = () => {}) {
    this.pool.query(
      'DELETE FROM sessions WHERE sid = $1',
      [sid]
    ).then(() => callback(null)).catch(callback);
  }

  touch(sid, sess, callback = () => {}) {
    const expired = sess.cookie?.expires
      ? new Date(sess.cookie.expires).getTime()
      : Date.now() + 8 * 60 * 60 * 1000;

    this.pool.query(
      'UPDATE sessions SET expired = $1 WHERE sid = $2',
      [expired, sid]
    ).then(() => callback(null)).catch(callback);
  }

  async cleanup() {
    await this.pool.query(
      'DELETE FROM sessions WHERE expired <= $1',
      [Date.now()]
    );
  }
}

module.exports = PostgresSessionStore;
