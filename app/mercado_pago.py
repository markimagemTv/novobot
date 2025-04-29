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
            "email": f"user{user_id}@email.com"  # Mesmo fictício, o e-mail é obrigatório
        },
        "notification_url": "https://seuservidor.com/notificacao"  # Opcional, mas recomendado
    }

    try:
        payment_response = sdk.payment().create(preference_data)
        payment = payment_response["response"]

        if payment.get("status") == "pending":
            qr_info = payment["point_of_interaction"]["transaction_data"]
            return {
                "pix_code": qr_info["qr_code"],
                "qr_image": qr_info["qr_code_base64"]
            }
        else:
            print(f"[ERRO] Status inesperado: {payment.get('status')}")
            return None
    except Exception as e:
        print(f"[ERRO] Falha ao gerar pagamento PIX: {e}")
        return None

