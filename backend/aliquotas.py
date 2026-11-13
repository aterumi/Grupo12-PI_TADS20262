from decimal import Decimal

# Alíquotas armazenadas como fração decimal (ex: 0.07 = 7%)
# Valores ilustrativos para a Prova de Conceito (PoC)
CATEGORIAS_TRIBUTOS = {
    "hortifruti_in_natura": {
        "nome": "Hortifrúti In Natura (Frutas, Verduras, Legumes)",
        "descricao": "Produtos frescos sem processamento industrial (ex: Tomate, Alface, Banana)",
        "aliquotas": {
            "ICMS": Decimal("0.00"),    # Isenção comum na cesta básica/hortifrúti
            "PIS": Decimal("0.00"),     # Alíquota zero (Lei 10.925/2004)
            "COFINS": Decimal("0.00"),  # Alíquota zero (Lei 10.925/2004)
            "ISS": Decimal("0.00")
        }
    },
    "hortifruti_minimamente_processado": {
        "nome": "Hortifrúti Minimamente Processado / Embalado",
        "descricao": "Produtos higienizados, cortados ou embalados para venda",
        "aliquotas": {
            "ICMS": Decimal("0.07"),    # 7.00%
            "PIS": Decimal("0.0165"),   # 1.65%
            "COFINS": Decimal("0.076"), # 7.60%
            "ISS": Decimal("0.00")
        }
    },
    "polpas_e_derivados": {
        "nome": "Polpas, Sucos Naturais e Derivados",
        "descricao": "Produtos processados a partir de frutas e vegetais",
        "aliquotas": {
            "ICMS": Decimal("0.12"),    # 12.00%
            "PIS": Decimal("0.0165"),   # 1.65%
            "COFINS": Decimal("0.076"), # 7.60%
            "ISS": Decimal("0.00")
        }
    },
    "servico_entrega": {
        "nome": "Serviço de Entrega / Frete Local",
        "descricao": "Serviço de transporte municipal de mercadorias",
        "aliquotas": {
            "ICMS": Decimal("0.00"),
            "PIS": Decimal("0.0065"),   # 0.65%
            "COFINS": Decimal("0.03"),  # 3.00%
            "ISS": Decimal("0.05")      # 5.00%
        }
    }
}