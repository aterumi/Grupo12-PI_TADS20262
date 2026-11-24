# API de Cálculo de Tributos Embutidos no Preço Final da Mercadoria

**Projeto Integrador — Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web**  
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas (TADS) — Centro Universitário SENAC EAD  
**Semestre/Ano:** 2026/2  
**Grupo:** Grupo 12  

---

## 1. Visão Geral e Prova de Conceito (PoC)

Este projeto consiste em uma solução híbrida (Web API REST + banco de dados relacional + interface web/mobile simplificada) desenvolvida para auxiliar pequenos empreendedores e comerciantes — com foco inicial no setor de **hortifrúti** — a compreenderem e simularem o percentual e o valor monetário dos tributos embutidos no preço final de venda de suas mercadorias e serviços (ICMS, PIS, COFINS e ISS).

### Justificativa e Escopo da PoC (2ª Etapa)
A partir do levantamento de requisitos e das jornadas de usuários mapeadas na 1ª Entrega (**Antônio Pereira**, baixa familiaridade tecnológica; e **Marcos Oliveira**, familiaridade intermediária), esta Prova de Conceito valida a viabilidade técnica do núcleo do sistema:
* **Cadastro simplificado de empresas/empreendedores** (`cadastro.html` / `cadastro.py`) persistido em banco de dados SQLite;
* **Consulta de categorias de produtos e serviços** com descrições diretas e isentas de jargões contábeis;
* **Simulação exata de tributos embutidos**, utilizando o tipo `Decimal` (`ROUND_HALF_UP`) no backend Python para eliminar erros de arredondamento financeiro e detalhar quanto do preço final corresponde a cada imposto e quanto permanece líquido para o comércio.

📄 **Documentação de Planejamento (1ª Entrega):** [Acessar Documento de Requisitos e Personas](./docs/PI-entrega%201-revisado.pdf)

---

## 2. Stack Tecnológica

* **Backend:** Python 3.12+ e FastAPI
* **Servidor ASGI:** Uvicorn
* **Banco de Dados:** SQLite (`empresas.db`)
* **Precisão Monetária:** Módulo nativo `decimal` (`Decimal`)
* **Frontend:** HTML5, CSS3 e JavaScript modularizado (interface responsiva com botões ampliados para acessibilidade)
* **Controle de Versão:** Git e GitHub

---

## 3. Estrutura de Diretórios

```text
Grupo12-PI_TADS20262/
├── backend/
│   ├── aliquotas.py        # Tabela isolada de categorias e alíquotas tributárias
│   ├── cadastro.py         # Lógica e rotas de cadastro e consulta de empresas
│   ├── main.py             # Aplicação FastAPI, regras de cálculo e integração dos endpoints
│   └── requirements.txt    # Dependências Python do projeto
├── database/
│   └── empresas.db         # Banco de dados SQLite com os registros de empresas
├── docs/
│   └── PI-entrega 1-revisado.pdf  # Documentação de planejamento, escopo e personas (1ª Entrega)
├── frontend/
│   ├── cadastro.html       # Tela de cadastro de empresas/empreendedores
│   ├── cadastro.js         # Lógica de integração do formulário de cadastro com a API
│   ├── index.html          # Tela principal de simulação de tributos embutidos
│   ├── script.js           # Lógica de consumo dos endpoints de simulação e categorias
│   └── style.css           # Folha de estilos unificada e responsiva da interface
├── .gitignore              # Arquivos e diretórios ignorados no versionamento (venv/, __pycache__/)
├── LICENSE                 # Licença do repositório
└── README.md               # Guia técnico e instruções de execução do projeto
```

---

## 4. Passo a Passo para Execução Local

### Pré-requisitos
* **Python 3.10 ou superior** instalado (com a opção *Add Python to PATH* marcada);
* Navegador web  (Chrome, Edge, Firefox ou Safari).

### Passo 1: Clonar o Repositório
Abra o terminal e execute:

```bash
git clone https://github.com/aterumi/Grupo12-PI_TADS20262.git
cd Grupo12-PI_TADS20262
```

### Passo 2: Configurar o Ambiente Virtual e Instalar Dependências
1. Acesse o diretório do backend:

```bash
cd backend
```

2. Crie e ative o ambiente virtual (`venv`):
* **Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

* **Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as bibliotecas listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Passo 3: Banco de Dados (SQLite)
* O banco de dados relacional já está estruturado e incluído no repositório em `database/empresas.db`, dispensando configuração externa de servidor de banco de dados. Ao iniciar a API, a conexão com o SQLite é realizada automaticamente.

### Passo 4: Iniciar o Servidor Backend (API)
Com o ambiente `(venv)` ativo dentro da pasta `backend/`, inicie o servidor Uvicorn:

```bash
uvicorn main:app --reload
```

* **Endereço base da API:** `http://127.0.0.1:8000`
* **Documentação interativa (Swagger UI):** `http://127.0.0.1:8000/docs`

### Passo 5: Executar o Frontend
1. Com o servidor backend ativo no terminal, abra a pasta `frontend/` no explorador de arquivos.
2. Abra o arquivo `index.html` no navegador para realizar a simulação de tributos ou navegue até `cadastro.html` para registrar uma nova empresa.

---

## 5. Principais Funcionalidades e Endpoints REST

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Verifica o status de disponibilidade da API. |
| `GET` | `/categorias` | Lista as categorias de mercadorias/serviços e suas descrições. |
| `POST` | `/simular` | Calcula os tributos embutidos (ICMS, PIS, COFINS, ISS) a partir do preço final informado. |
| `POST` / `GET` | `/empresas` | Realiza o cadastro e a consulta de empresas no banco de dados SQLite (`cadastro.py`). |

*(Consulte todas as rotas e esquemas JSON em tempo real acessando `http://127.0.0.1:8000/docs` com o servidor em execução).*

---

## 6. Demonstração em Vídeo

* **Vídeo de Apresentação e Funcionamento ** *https://youtu.be/uTkQc37ufqM*

---

## 7. Integrantes do Grupo 12

* Allan Alves Menezes
* Amanda Sartoreli Borcsik
* Angela Terumi Fushita
* Gabriel Lima Lucas Santos
* Monique Veloso de Jesus
* Raphael Alves Vieira

---

> **Aviso Legal:** Os cálculos e alíquotas apresentados nesta Prova de Conceito têm finalidade estritamente acadêmica, estimativa e informativa, não substituindo a orientação de um profissional de contabilidade.
