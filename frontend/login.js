document.getElementById('formLogin').addEventListener('submit', async function(e) {
    e.preventDefault();

    const msgDiv = document.getElementById('mensagem');
    const btn = document.getElementById('btnEntrar');
    msgDiv.textContent = "Processando login...";
    msgDiv.className = "msg";
    if (btn) btn.disabled = true;

    const dados = {
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value
    };

    try {
        const resposta = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            msgDiv.textContent = "Login realizado com sucesso! Redirecionando...";
            msgDiv.className = "msg success";

            localStorage.setItem('empresa_id', resultado.empresa_id);
            localStorage.setItem('nome_empresa', resultado.nome_empresa);
            localStorage.setItem('empresa_email', resultado.email);

            setTimeout(() => {
                window.location.href = '/';
            }, 1200);
        } else {
            msgDiv.textContent = resultado.detail || "E-mail ou senha inválidos.";
            msgDiv.className = "msg error";
            if (btn) btn.disabled = false;
        }
    } catch (error) {
        console.error("Erro:", error);
        msgDiv.textContent = "Não foi possível conectar ao servidor.";
        msgDiv.className = "msg error";
        if (btn) btn.disabled = false;
    }
});
