document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const btnLogin = document.getElementById('btn-login');
  const feedback = document.getElementById('login-feedback');
  const cardSessao = document.getElementById('card-sessao-ativa');
  const sessaoNome = document.getElementById('sessao-empresa-nome');
  const sessaoEmail = document.getElementById('sessao-empresa-email');
  const btnLogout = document.getElementById('btn-logout');

  function atualizarCardSessao() {
    const empresaId = localStorage.getItem('empresa_id');
    const nomeEmpresa = localStorage.getItem('nome_empresa');
    const emailEmpresa = localStorage.getItem('empresa_email');

    if (empresaId && nomeEmpresa) {
      if (sessaoNome) sessaoNome.textContent = nomeEmpresa;
      if (sessaoEmail) sessaoEmail.textContent = emailEmpresa || '';
      if (cardSessao) cardSessao.style.display = 'block';
    } else {
      if (cardSessao) cardSessao.style.display = 'none';
    }
  }

  function exibirMensagem(texto, tipo) {
    if (!feedback) return;
    feedback.textContent = texto;
    feedback.className = `auth-feedback ${tipo}`;
    feedback.style.display = 'block';
  }

  function limparMensagem() {
    if (!feedback) return;
    feedback.textContent = '';
    feedback.className = 'auth-feedback';
    feedback.style.display = 'none';
  }

  // Verifica se já há sessão ativa
  atualizarCardSessao();

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      limparMensagem();

      const email = document.getElementById('email').value.trim();
      const senha = document.getElementById('senha').value;

      if (!email || !senha) {
        exibirMensagem('Por favor, preencha todos os campos.', 'error');
        return;
      }

      btnLogin.disabled = true;
      btnLogin.textContent = 'Autenticando...';

      try {
        const response = await fetch('/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (response.ok) {
          localStorage.setItem('empresa_id', String(data.empresa_id));
          localStorage.setItem('nome_empresa', data.nome_empresa);
          localStorage.setItem('empresa_email', data.email);

          exibirMensagem(`Bem-vindo, ${data.nome_empresa}! Redirecionando para o Dashboard...`, 'success');
          atualizarCardSessao();

          setTimeout(() => {
            window.location.href = '/';
          }, 1200);
        } else {
          const erroMsg = data.detail || 'Falha ao autenticar. Verifique seus dados.';
          exibirMensagem(erroMsg, 'error');
          btnLogin.disabled = false;
          btnLogin.textContent = 'Entrar na Plataforma';
        }
      } catch (err) {
        console.error('Erro de conexão:', err);
        exibirMensagem('Não foi possível conectar ao servidor. Verifique se a API está em execução.', 'error');
        btnLogin.disabled = false;
        btnLogin.textContent = 'Entrar na Plataforma';
      }
    });
  }

  if (btnLogout) {
    btnLogout.addEventListener('click', () => {
      localStorage.removeItem('empresa_id');
      localStorage.removeItem('nome_empresa');
      localStorage.removeItem('empresa_email');
      atualizarCardSessao();
      exibirMensagem('Você desconectou da sua conta.', 'success');
    });
  }
});
