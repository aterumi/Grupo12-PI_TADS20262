from decimal import Decimal
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import os

app = FastAPI(
    title="API de Cálculo de Tributos Embutidos",
    description="Web API para simulação da carga tributária embutida no preço final de mercadorias e serviços (Setor de Hortifrúti).",
    version="1.0.0",
)

# Configuração de CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de dados de alíquotas adaptada para a interface fornecida
CATEGORIAS_TRIBUTOS: Dict[str, Dict[str, Any]] = {
    "frutas": {
        "nome": "Frutas",
        "ICMS": Decimal("4.00"),
        "PIS": Decimal("0.65"),
        "COFINS": Decimal("3.00"),
        "ISS": Decimal("0.00"),
    },
    "verduras": {
        "nome": "Verduras",
        "ICMS": Decimal("2.00"),
        "PIS": Decimal("0.65"),
        "COFINS": Decimal("3.00"),
        "ISS": Decimal("0.00"),
    },
    "legumes": {
        "nome": "Legumes",
        "ICMS": Decimal("3.00"),
        "PIS": Decimal("0.65"),
        "COFINS": Decimal("3.00"),
        "ISS": Decimal("0.00"),
    },
    "tuberculos": {
        "nome": "Tubérculos",
        "ICMS": Decimal("3.50"),
        "PIS": Decimal("0.65"),
        "COFINS": Decimal("3.00"),
        "ISS": Decimal("0.00"),
    },
}


class CalcularRequest(BaseModel):
  categoria_id: str
  preco_venda: Decimal = Field(..., gt=0)


@app.get(
    "/", response_class=HTMLResponse, summary="Página Principal da Interface"
)
def serve_frontend():
  if os.path.exists("projeto.html"):
    with open("projeto.html", "r", encoding="utf-8") as f:
      return f.read()
  return (
      "<h1>API Operante</h1><p>Coloque o arquivo projeto.html na mesma"
      " pasta do main.py para carregar a interface automaticamente.</p>"
  )


@app.get("/api/categorias", summary="Listar Categorias para a Interface")
def api_categorias():
  resultado = {}
  for k, v in CATEGORIAS_TRIBUTOS.items():
    resultado[k] = {
        "nome": v["nome"],
        "ICMS": float(v["ICMS"]),
        "PIS": float(v["PIS"]),
        "COFINS": float(v["COFINS"]),
        "ISS": float(v["ISS"]),
    }
  return resultado


@app.post("/api/calcular", summary="Calcular Impostos Embutidos")
def api_calcular(dados: CalcularRequest):
  cat_id = dados.categoria_id.strip().lower()
  if cat_id not in CATEGORIAS_TRIBUTOS:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"erro": f"Categoria '{dados.categoria_id}' não encontrada."},
    )

  cat_info = CATEGORIAS_TRIBUTOS[cat_id]
  preco = dados.preco_venda

  aliq_icms = cat_info["ICMS"]
  aliq_pis = cat_info["PIS"]
  aliq_cofins = cat_info["COFINS"]
  aliq_iss = cat_info["ISS"]

  val_icms = (preco * aliq_icms) / Decimal("100")
  val_pis = (preco * aliq_pis) / Decimal("100")
  val_cofins = (preco * aliq_cofins) / Decimal("100")
  val_iss = (preco * aliq_iss) / Decimal("100")

  percentual_total = aliq_icms + aliq_pis + aliq_cofins + aliq_iss
  valor_tributos_total = val_icms + val_pis + val_cofins + val_iss
  valor_liquido = preco - valor_tributos_total

  return {
      "categoria": cat_info["nome"],
      "preco_venda": float(preco),
      "percentual_total": float(percentual_total),
      "valor_tributos_total": float(
          valor_tributos_total.quantize(Decimal("0.01"))
      ),
      "valor_liquido": float(valor_liquido.quantize(Decimal("0.01"))),
      "detalhes": {
          "icms": {
              "aliquota": float(aliq_icms),
              "valor": float(val_icms.quantize(Decimal("0.01"))),
          },
          "pis": {
              "aliquota": float(aliq_pis),
              "valor": float(val_pis.quantize(Decimal("0.01"))),
          },
          "cofins": {
              "aliquota": float(aliq_cofins),
              "valor": float(val_cofins.quantize(Decimal("0.01"))),
          },
          "iss": {
              "aliquota": float(aliq_iss),
              "valor": float(val_iss.quantize(Decimal("0.01"))),
          },
          "ISS": {
              "aliquota": float(aliq_iss),
              "valor": float(val_iss.quantize(Decimal("0.01"))),
          },
      },
  }