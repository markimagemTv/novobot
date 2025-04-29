import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # URL pública do Render ou Heroku

# Validações
if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN não definido no .env")

if not ADMIN_CHAT_ID:
    raise ValueError("⚠️ ADMIN_CHAT_ID não definido no .env")
else:
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)

if not MP_ACCESS_TOKEN:
    raise ValueError("⚠️ MP_ACCESS_TOKEN não definido no .env")

if not BASE_URL:
    print("🔔 Aviso: BASE_URL não foi definido. Algumas integrações podem não funcionar.")
