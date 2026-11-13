# Grupo12-PI_TADS20262
Repositório da 2ª Etapa do Projeto Integrador (TADS-SENAC) - Web API de Cálculo de Tributo<br>

Projeto Integrador apresentado ao Centro Universitário SENAC - Serviço Nacional de Aprendizagem Comercial, como requisito de avaliação semestral do curso de Tecnologia em Análise e Desenvolvimento de Sistemas.


# API de Cálculo de Tributos Embutidos no Preço Final da Mercadoria

**Projeto Integrador — Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web**  
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas (TADS) — Centro Universitário SENAC EAD  
**Semestre/Ano:** 2026/2  
**Grupo:** Grupo 12  
**Componentes:**
Allan Alves Menezes
Amanda Sartoreli Borcsik
Angela Terumi Fushita
Gabriel Lima Lucas Santos
Monique Veloso de Jesus
Raphael Alves Vieira

---

## 1. Sobre o Projeto e Prova de Conceito (PoC)

Este projeto consiste em uma solução híbrida (Web API REST + interface simplificada responsiva) desenvolvida para auxiliar pequenos empreendedores e comerciantes — com foco inicial no setor de **hortifruti** — a compreenderem e simularem o percentual e o valor monetário dos tributos embutidos no preço final de venda de suas mercadorias e serviços (ICMS, PIS, COFINS e ISS).

### Escopo da Prova de Conceito (PoC — 2ª Entrega)
Com base no levantamento de requisitos e personas da 1ª Entrega (**Antônio Pereira**, baixa familiaridade tecnológica; e **Marcos Oliveira**, familiaridade intermediária), esta PoC implementa a jornada principal de **simulação rápida de tributos embutidos por categoria de produto**:
* Seleção simplificada da categoria de produto/serviço com descrição explicativa;
* Entrada do preço final de venda praticado;
* Cálculo exato (utilizando o tipo `Decimal` para evitar erros de arredondamento financeiro) e exibição clara do valor total dos tributos, do valor líquido estimado que permanece para o comércio e do detalhamento por imposto[cite: 17, 18].

---

## 2. Tecnologias Utilizadas

* **Backend:** Python 3.12+ e FastAPI[cite: 18]
* **Servidor ASGI:** Uvicorn
* **Precisão Monetária:** Módulo nativo `decimal` (`Decimal` e `ROUND_HALF_UP`)
* **Frontend:** HTML5, CSS3 e JavaScript (Vanilla JS com Fetch API)[cite: 18]
* **Versionamento:** Git e GitHub[cite: 9]

---

## 3. Estrutura de Diretórios

```text
Grupo12-PI_TADS20262/
├── backend/
│   ├── aliquotas.py        # Tabela isolada de categorias e alíquotas tributárias
│   ├── main.py             # Aplicação FastAPI, regras de cálculo e endpoints REST
│   └── requirements.txt    # Dependências Python do projeto
├── frontend/
│   └── index.html          # Interface web/mobile simplificada para consulta e simulação
├── database/               # Diretório reservado para scripts e persistência de dados
├── docs/                   # Documentação complementar do projeto
├── .gitignore              # Arquivos e pastas ignorados no versionamento (ex: venv/)
└── README.md               # Documentação principal e guia de execução

---
## 4. Instruções de Execução (Passo a Passo)
Pré-requisitos
Python 3.10 ou superior instalado na máquina (com a opção Add Python to PATH habilitada);

Navegador web moderno (Chrome, Edge, Firefox ou Safari).

Passo 1: Clonar o Repositório
git clone [https://github.com/aterumi/Grupo12-PI_TADS20262.git](https://github.com/aterumi/Grupo12-PI_TADS20262.git)
cd Grupo12-PI_TADS20262

Passo 2: Configurar e Iniciar o Servidor Backend (API)
Acesse a pasta backend:

cd backend
Crie e ative o ambiente virtual (venv):

No Windows:
python -m venv venv
venv\Scripts\activate

No Linux / macOS:
python3 -m venv venv
source venv/bin/activate

Instale as dependências necessárias:
pip install -r requirements.txt

Inicie o servidor local da API:
uvicorn main:app --reload

O servidor estará ativo em: http://127.0.0.1:8000

A documentação interativa (Swagger UI) pode ser acessada em: http://127.0.0.1:8000/docs

Passo 3: Executar a Interface Frontend
Com o servidor backend rodando no terminal, navegue até a pasta frontend/ no explorador de arquivos do seu computador.

Dê um duplo clique no arquivo index.html para abri-lo em seu navegador padrão.

Selecione uma categoria (ex.: Hortifruti Minimamente Processado / Embalado), informe um preço de venda (ex.: 25.00) e clique em Calcular Impostos.

## 5. Documentação dos Endpoints da API
Método  Rota              Descrição
GET     /               Verifica o status de funcionamento da API.
GET     /categorias     Retorna a lista de categorias de produtos/serviços cadastradas e suas descrições.
POST    /simular        Recebe o ID da categoria e o preço final de venda, retornando o cálculo detalhado dos tributos embutidos.

Exemplo de Requisição (POST /simular)
Corpo enviado (JSON):
{
  "categoria_id": "hortifruti_minimamente_processado",
  "preco_final": 25.00
}

Resposta retornada (JSON):
{
  "categoria": "Hortifrúti Minimamente Processado / Embalado",
  "preco_final_informado": 25.0,
  "total_tributos_percentual": "16.25%",
  "total_tributos_valor": 4.06,
  "valor_liquido_estimado": 20.94,
  "detalhamento_por_tributo": [
    { "tributo": "ICMS", "percentual": "7.00%", "valor_embutido": 1.75 },
    { "tributo": "PIS", "percentual": "1.65%", "valor_embutido": 0.41 },
    { "tributo": "COFINS", "percentual": "7.60%", "valor_embutido": 1.90 },
    { "tributo": "ISS", "percentual": "0.00%", "valor_embutido": 0.00 }
  ],
  "aviso": "Valores estimativos e informativos; não substituem orientação contábil."
}

## 6. Demonstração em Vídeo
Link do vídeo de demonstração 

## 7. Integrantes do Grupo 12
Allan Alves Menezes
Amanda Sartoreli Borcsik
Angela Terumi Fushita
Gabriel Lima Lucas Santos
Monique Veloso de Jesus
Raphael Alves Vieira

Aviso Legal: Os valores e alíquotas apresentados nesta Prova de Conceito têm caráter estritamente acadêmico, estimativo e informativo, não substituindo a orientação de um profissional de contabilidade

