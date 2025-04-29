import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
BASE_URL = os.getenv("BASE_URL")
