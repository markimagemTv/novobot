import telebot
from app.config import BOT_TOKEN
from app.handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN)
register_handlers(bot)

def run_bot():
    bot.polling()
