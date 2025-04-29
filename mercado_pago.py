import mercadopago
from app.config import MP_ACCESS_TOKEN, BASE_URL

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
    preference_response = sdk.preference().create(preference_data)
    return preference_response["response"]["init_point"]
