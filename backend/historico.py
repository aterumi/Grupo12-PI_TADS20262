import json
import os
import sqlite3
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

router = APIRouter(tags=["Histórico Fiscal"])

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../database/empresas.db")
)


class HistoricoCreateSchema(BaseModel):
    empresa_id: int
    categoria_id: str | None = None
    categoria_nome: str
    preco_informado: float
    total_tributos_percentual: str
    total_tributos_valor: float
    valor_liquido: float
    resultado_json: dict | None = None


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def criar_tabela_historico():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS historico_consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa_id INTEGER NOT NULL,
                categoria_id TEXT,
                categoria_nome TEXT NOT NULL,
                preco_informado REAL NOT NULL,
                total_tributos_percentual TEXT NOT NULL,
                total_tributos_valor REAL NOT NULL,
                valor_liquido REAL NOT NULL,
                resultado_json TEXT,
                data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()


criar_tabela_historico()


def salvar_consulta_no_historico(dados: HistoricoCreateSchema) -> int:
    criar_tabela_historico()
    with get_connection() as conn:
        cursor = conn.cursor()

        empresa = cursor.execute(
            "SELECT id FROM empresas WHERE id = ?", (dados.empresa_id,)
        ).fetchone()
        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada para vincular ao histórico.",
            )

        cursor.execute(
            """
            INSERT INTO historico_consultas (
                empresa_id,
                categoria_id,
                categoria_nome,
                preco_informado,
                total_tributos_percentual,
                total_tributos_valor,
                valor_liquido,
                resultado_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dados.empresa_id,
                dados.categoria_id,
                dados.categoria_nome,
                dados.preco_informado,
                dados.total_tributos_percentual,
                dados.total_tributos_valor,
                dados.valor_liquido,
                json.dumps(dados.resultado_json, ensure_ascii=False)
                if dados.resultado_json is not None
                else None,
            ),
        )
        conn.commit()
        return cursor.lastrowid


@router.post("/historico", status_code=status.HTTP_201_CREATED)
def criar_historico(dados: HistoricoCreateSchema):
    consulta_id = salvar_consulta_no_historico(dados)
    return {
        "mensagem": "Consulta salva no histórico com sucesso.",
        "id": consulta_id,
    }


@router.get("/historico")
def listar_historico(empresa_id: int = Query(..., gt=0)):
    criar_tabela_historico()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                empresa_id,
                categoria_id,
                categoria_nome,
                preco_informado,
                total_tributos_percentual,
                total_tributos_valor,
                valor_liquido,
                resultado_json,
                data_consulta
            FROM historico_consultas
            WHERE empresa_id = ?
            ORDER BY id DESC
            """,
            (empresa_id,),
        ).fetchall()

    historico = []
    for row in rows:
        item = dict(row)
        if item.get("resultado_json"):
            try:
                item["resultado_json"] = json.loads(item["resultado_json"])
            except Exception:
                pass
        historico.append(item)

    return historico


@router.delete("/historico")
def limpar_historico(empresa_id: int = Query(..., gt=0)):
    criar_tabela_historico()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM historico_consultas WHERE empresa_id = ?",
            (empresa_id,),
        )
        conn.commit()
        removidos = cursor.rowcount

    return {
        "mensagem": "Histórico limpo com sucesso.",
        "registros_removidos": removidos,
    }