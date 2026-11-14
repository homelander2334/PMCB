const readline = require('node:readline/promises');
const { stdin, stdout } = require('node:process');

async function hidden(prompt) {
  stdout.write(prompt);
  stdin.setRawMode(true);
  stdin.resume();
  stdin.setEncoding('utf8');

  return new Promise(resolve => {
    let value = '';
    function finish() {
      stdin.removeListener('data', onData);
      stdin.setRawMode(false);
      stdin.pause();
      stdout.write('\n');
      resolve(value);
    }
    function onData(char) {
      if (char === '\u0003') {
        finish();
        process.exit(1);
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

function cookieFrom(response, fallback) {
  const cookies = response.headers.getSetCookie?.() || [];
  return cookies.length ? cookies[0].split(';')[0] : fallback;
}

async function main() {
  const rl = readline.createInterface({ input: stdin, output: stdout });
  const email = await rl.question('E-mail administrativo: ');
  rl.close();
  const password = await hidden('Senha: ');

  const base = 'http://127.0.0.1:3000';
  const csrf = await fetch(base + '/api/csrf');
  let cookie = cookieFrom(csrf);
  const initialToken = (await csrf.json()).csrfToken;

  const login = await fetch(base + '/api/admin/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': cookie,
      'x-csrf-token': initialToken
    },
    body: JSON.stringify({ email, password })
  });

  console.log('Login HTTP:', login.status);
  const loginData = await login.json();

  if (!login.ok) {
    console.log('Mensagem:', loginData.message);
    return;
  }

  cookie = cookieFrom(login, cookie);
  console.log('Autenticação:', loginData.success ? 'aprovada' : 'falhou');
  console.log('Papel:', loginData.admin?.role);

  const me = await fetch(base + '/api/admin/me', {
    headers: { Cookie: cookie }
  });
  console.log('Consulta da sessão HTTP:', me.status);

  const logout = await fetch(base + '/api/admin/logout', {
    method: 'POST',
    headers: {
      Cookie: cookie,
      'x-csrf-token': loginData.csrfToken
    }
  });
  console.log('Logout HTTP:', logout.status);

  const after = await fetch(base + '/api/admin/me', {
    headers: { Cookie: cookie }
  });
  console.log('Sessão após logout HTTP:', after.status);
  console.log('Esperado após logout: 401');
}

main().catch(error => {
  console.error('Teste não concluído:', error.message);
  process.exitCode = 1;
});
