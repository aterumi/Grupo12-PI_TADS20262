from fastapi import FastAPI
from decimal import Decimal

app = FastAPI(title="API de Cálculo de Tributos Embutidos - Hortifrúti")

@app.get("/")
def verificar_servidor():
    return {
        "status": "OK",
        "mensagem": "Servidor Python da API de Tributos rodando!",
        "exemplo_precisao": str(Decimal("10.00"))
    }