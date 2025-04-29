import mercadopago
from app.config import MP_ACCESS_TOKEN, BASE_URL

if not MP_ACCESS_TOKEN:
    raise ValueError("⚠️ MP_ACCESS_TOKEN não foi definido no .env")

if not BASE_URL:
    raise ValueError("⚠️ BASE_URL não foi definido no .env")

sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

def gerar_link_pagamento(nome_produto, valor, user_id):
    preference_data = {
        "items": [{
            "title": nome_produto,
            "quantity": 1,
            "unit_price": float(valor)
        }],
        "notification_url": f"{BASE_URL}/pagamento/webhook",
        "external_reference": str(user_id)
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        return preference_response["response"].get("init_point", "Erro: init_point não retornado")
    except Exception as e:
        print(f"Erro ao gerar link de pagamento: {e}")
        return None
