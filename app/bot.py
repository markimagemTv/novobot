import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import telebot
from app.config import BOT_TOKEN
from app.handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN)
register_handlers(bot)

if __name__ == "__main__":
    bot.polling()
