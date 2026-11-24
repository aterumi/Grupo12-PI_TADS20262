document.getElementById('formCadastro').addEventListener('submit', async function(e) {
    e.preventDefault();

    const msgDiv = document.getElementById('mensagem');
    msgDiv.textContent = "Processando cadastro...";
    msgDiv.className = "msg";

    const dados = {
        nome_empresa: document.getElementById('nome_empresa').value,
        cnpj: document.getElementById('cnpj').value || null,
        email: document.getElementById('email').value,
        telefone: document.getElementById('telefone').value,
        cep: document.getElementById('cep').value,
        endereco: document.getElementById('endereco').value,
        numero: "S/N", // Caso queira separar rua/numero depois, por ora coletamos integrado
        complemento: document.getElementById('complemento').value || null,
        cidade: document.getElementById('cidade').value,
        uf: document.getElementById('uf').value.toUpperCase(),
        senha: document.getElementById('senha').value
    };

    try {
        const resposta = await fetch('http://127.0.0.1:8000/cadastro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            msgDiv.textContent = "Cadastro realizado com sucesso! Redirecionando para o login...";
            msgDiv.className = "msg success";
            setTimeout(() => {
                window.location.href = '/login';
            }, 1500);
        } else {
            msgDiv.textContent = resultado.detail || "Erro ao realizar o cadastro.";
            msgDiv.className = "msg error";
        }
    } catch (error) {
        console.error("Erro:", error);
        msgDiv.textContent = "Não foi possível conectar ao servidor.";
        msgDiv.className = "msg error";
    }
});