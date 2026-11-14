const readline = require('node:readline/promises');
const { stdin, stdout } = require('node:process');
const db = require('../server/database');
const { createAdmin } = require('../server/auth');

async function readHidden(prompt) {
  if (!stdin.isTTY || typeof stdin.setRawMode !== 'function') {
    throw new Error('Execute este script diretamente no terminal do Termux.');
  }

  stdout.write(prompt);
  stdin.setRawMode(true);
  stdin.resume();
  stdin.setEncoding('utf8');

  return new Promise((resolve, reject) => {
    let value = '';

    function finish(error) {
      stdin.removeListener('data', onData);
      stdin.setRawMode(false);
      stdin.pause();
      stdout.write('\n');

      if (error) reject(error);
      else resolve(value);
    }

    function onData(char) {
      if (char === '\u0003') {
        finish(new Error('Operação cancelada.'));
      } else if (char === '\r' || char === '\n') {
        finish();
      } else if (char === '\u007f' || char === '\b') {
        value = value.slice(0, -1);
      } else if (char >= ' ') {
        value += char;
      }
    }

    stdin.on('data', onData);
  });
}

async function main() {
  const total = db.prepare(
    'SELECT COUNT(*) AS total FROM admin_users'
  ).get().total;

  if (total > 0) {
    throw new Error('Já existe um administrador. Cadastro inicial bloqueado.');
  }

  const rl = readline.createInterface({ input: stdin, output: stdout });

  try {
    const name = await rl.question('Nome do superadministrador: ');
    const email = await rl.question('E-mail administrativo: ');
    rl.close();

    const password = await readHidden('Senha (mínimo 12 caracteres): ');
    const confirmation = await readHidden('Confirme a senha: ');

    if (password !== confirmation) {
      throw new Error('As senhas não coincidem.');
    }

    const id = await createAdmin({
      name,
      email,
      password,
      role: 'superadmin'
    });

    console.log('Superadministrador criado com sucesso. ID:', id);
    console.log('Guarde suas credenciais em local seguro.');
  } finally {
    if (!rl.closed) rl.close();
  }
}

main().catch(error => {
  console.error('Cadastro não concluído:', error.message);
  process.exitCode = 1;
});
