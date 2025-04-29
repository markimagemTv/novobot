import mercadopago
import os
from dotenv import load_dotenv

load_dotenv()

sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN"))

def gerar_pagamento_pix(descricao, valor, user_id):
    preference_data = {
        "transaction_amount": float(valor),
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": f"user{user_id}@email.com"
        }
    }

    payment = sdk.payment().create(preference_data)

    if payment["status"] == 201:
        qr_info = payment["response"]["point_of_interaction"]["transaction_data"]
        return {
            "pix_code": qr_info["qr_code"],
            "qr_image": qr_info["qr_code_base64"]
        }
    else:
        return None
