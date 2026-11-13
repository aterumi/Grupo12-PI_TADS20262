from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from decimal import Decimal, ROUND_HALF_UP
from aliquotas import CATEGORIAS_TRIBUTOS

app = FastAPI(
    title="API de Cálculo de Tributos Embutidos",
    description="Web API para cálculo percentual e monetário de tributos embutidos no preço final (Hortifrúti e Serviços).",
    version="1.0.0"
)

# Libera o acesso para que o Frontend (HTML/JS) consiga consumir a API sem bloqueio de navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada de dados para a simulação
class SimulacaoRequest(BaseModel):
    categoria_id: str = Field(..., example="hortifruti_minimamente_processado")
    preco_final: Decimal = Field(..., gt=0, example="25.00")

def arredondar_moeda(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

@app.get("/")
def status_api():
    return {"status": "online", "mensagem": "API de Tributos Embutidos ativa."}

# Endpoint 1: Listar categorias disponíveis para preencher a tela do usuário
@app.get("/categorias")
def listar_categorias():
    lista = []
    for chave, dados in CATEGORIAS_TRIBUTOS.items():
        lista.append({
            "id": chave,
            "nome": dados["nome"],
            "descricao": dados["descricao"]
        })
    return {"categorias": lista}

# Endpoint 2: Calcular tributos embutidos a partir do preço final
@app.post("/simular")
def simular_tributos(dados: SimulacaoRequest):
    categoria = CATEGORIAS_TRIBUTOS.get(dados.categoria_id)
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria de produto/serviço não encontrada.")

    preco = Decimal(str(dados.preco_final))
    aliquotas = categoria["aliquotas"]
    
    detalhamento = []
    total_impostos_valor = Decimal("0.00")
    total_impostos_percentual = Decimal("0.00")

    for tributo, aliquota in aliquotas.items():
        valor_tributo = arredondar_moeda(preco * aliquota)
        percentual_exibicao = (aliquota * Decimal("100")).quantize(Decimal("0.01"))
        
        total_impostos_valor += valor_tributo
        total_impostos_percentual += percentual_exibicao
        
        detalhamento.append({
            "tributo": tributo,
            "percentual": f"{percentual_exibicao}%",
            "valor_embutido": float(valor_tributo)
        })

    valor_liquido = arredondar_moeda(preco - total_impostos_valor)

    return {
        "categoria": categoria["nome"],
        "preco_final_informado": float(arredondar_moeda(preco)),
        "total_tributos_percentual": f"{total_impostos_percentual}%",
        "total_tributos_valor": float(total_impostos_valor),
        "valor_liquido_estimado": float(valor_liquido),
        "detalhamento_por_tributo": detalhamento,
        "aviso": "Valores estimativos e informativos; não substituem orientação contábil."
    }