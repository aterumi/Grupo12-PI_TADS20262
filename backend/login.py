import os
import sqlite3
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

router = APIRouter(tags=["Autenticação"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mesmo banco e tabela criados no cadastro.py
DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../database/empresas.db")
)


class LoginSchema(BaseModel):
    email: EmailStr
    senha: str


class LoginResponse(BaseModel):
    mensagem: str
    empresa_id: int
    nome_empresa: str
    email: EmailStr


def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_digitada, senha_hash)


@router.post("/login", response_model=LoginResponse)
def login_empresa(dados: LoginSchema):
    if not os.path.exists(DB_PATH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    email_limpo = dados.email.strip().lower()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, nome_empresa, email, senha_hash
            FROM empresas
            WHERE LOWER(email) = ?
            """,
            (email_limpo,),
        )
        empresa = cursor.fetchone()
    finally:
        conn.close()

    if not empresa or not verificar_senha(dados.senha, empresa["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    return LoginResponse(
        mensagem="Login realizado com sucesso!",
        empresa_id=empresa["id"],
        nome_empresa=empresa["nome_empresa"],
        email=empresa["email"],
    )