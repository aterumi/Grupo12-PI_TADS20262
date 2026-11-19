from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import sqlite3
import os

router = APIRouter()

# Configuração do Hash de Senha (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Caminho para o banco de dados na raiz do projeto
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/empresas.db"))

def criar_banco():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_empresa TEXT NOT NULL,
            cnpj TEXT UNIQUE,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            cep TEXT,
            endereco TEXT,
            numero TEXT,
            complemento TEXT,
            cidade TEXT,
            uf TEXT,
            senha_hash TEXT NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Executa a criação da tabela ao iniciar o módulo
criar_banco()

class CadastroSchema(BaseModel):
    nome_empresa: str
    cnpj: str | None = None
    email: EmailStr
    telefone: str
    cep: str
    endereco: str
    numero: str
    complemento: str | None = None
    cidade: str
    uf: str
    senha: str

@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar_empresa(dados: CadastroSchema):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se o e-mail já está cadastrado
    cursor.execute("SELECT id FROM empresas WHERE email = ?", (dados.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado no sistema."
        )

    # Passo 5: A senha é protegida por hash
    senha_hash = pwd_context.hash(dados.senha)

    try:
        cursor.execute("""
            INSERT INTO empresas (
                nome_empresa, cnpj, email, telefone, cep, 
                endereco, numero, complemento, cidade, uf, senha_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados.nome_empresa, dados.cnpj, dados.email, dados.telefone, dados.cep,
            dados.endereco, dados.numero, dados.complemento, dados.cidade, dados.uf, senha_hash
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao cadastrar. CNPJ já pode estar em uso."
        )
    finally:
        conn.close()

    return {"mensagem": "Empresa cadastrada com sucesso!"}