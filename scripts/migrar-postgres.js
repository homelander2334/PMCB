
const sqlite = require('../server/database');
const { db: postgres } = require('../server/database.pg');

async function migrar() {
  try {
    const administradores = sqlite.prepare(`
      SELECT id, name, email, password_hash, role, active,
             created_at, updated_at
      FROM admin_users
    `).all();

    if (administradores.length !== 1) {
      throw new Error(
        `Esperado 1 administrador no SQLite; encontrados: ${administradores.length}`
      );
    }

    const existente = await postgres.query(
      'SELECT COUNT(*)::int AS total FROM admin_users'
    );

    if (existente.rows[0].total !== 0) {
      throw new Error(
        'O Neon já possui administradores. Migração cancelada.'
      );
    }

    const admin = administradores[0];

    await postgres.query('BEGIN');

    try {
      const resultado = await postgres.query(
        `INSERT INTO admin_users
          (id, name, email, password_hash, role, active,
           created_at, updated_at)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
         RETURNING id, name, email, password_hash, role, active`,
        [
          admin.id,
          admin.name,
          admin.email,
          admin.password_hash,
          admin.role,
          admin.active,
          admin.created_at,
          admin.updated_at
        ]
      );

      const copiado = resultado.rows[0];

      if (
        Number(copiado.id) !== Number(admin.id) ||
        copiado.email !== admin.email ||
        copiado.password_hash !== admin.password_hash ||
        copiado.role !== admin.role ||
        Number(copiado.active) !== Number(admin.active)
      ) {
        throw new Error('A verificação dos dados falhou.');
      }

      await postgres.query(
        `SELECT setval(
          pg_get_serial_sequence('admin_users', 'id'),
          GREATEST(
            (SELECT COALESCE(MAX(id), 1) FROM admin_users),
            1
          )
        )`
      );

      await postgres.query('COMMIT');

      console.log('Migração do administrador concluída!');
      console.log('ID preservado:', copiado.id);
      console.log('Função preservada:', copiado.role);
      console.log('Hash da senha preservado: sim');
      console.log('Conta ativa:', Number(copiado.active) === 1);
    } catch (erro) {
      await postgres.query('ROLLBACK');
      throw erro;
    }
  } catch (erro) {
    console.error('Migração cancelada:', erro.message);
    process.exitCode = 1;
  } finally {
    sqlite.close();
    await postgres.end();
  }
}

migrar();

