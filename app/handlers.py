from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
from app.config import ADMIN_CHAT_ID
from app.mercado_pago import gerar_pagamento_pix
import base64

def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(msg: Message):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Mega IPTV - R$65", callback_data="comprar_iptv"))
        markup.add(InlineKeyboardButton("Comprar Créditos", callback_data="comprar_creditos"))
        bot.send_message(msg.chat.id, "Bem-vindo! Escolha uma opção:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        if call.data == "comprar_iptv":
            bot.send_message(call.message.chat.id, "Informe o MAC Address:")
            bot.register_next_step_handler(call.message, receber_mac)

        elif call.data == "comprar_creditos":
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("10 Créditos - R$5", callback_data="creditos_10"))
            markup.add(InlineKeyboardButton("20 Créditos - R$10", callback_data="creditos_20"))
            markup.add(InlineKeyboardButton("50 Créditos - R$25", callback_data="creditos_50"))
            bot.edit_message_text("Escolha o pacote de créditos:", call.message.chat.id, call.message.message_id, reply_markup=markup)

        elif call.data.startswith("creditos_"):
            quantidade = int(call.data.split("_")[1])
            valor = (quantidade // 10) * 5
            pagamento = gerar_pagamento_pix(f"{quantidade} Créditos Fast Play", valor, call.from_user.id)

            if pagamento:
                pix_code = pagamento["pix_code"]
                qr_base64 = pagamento["qr_image"]
                with open("temp_qr.png", "wb") as f:
                    f.write(base64.b64decode(qr_base64))

                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("✅ Copiar Código PIX", switch_inline_query=pix_code))

                bot.send_photo(call.message.chat.id, photo=open("temp_qr.png", "rb"),
                               caption=f"💳 *PIX Copia e Cola:*\n\n`{pix_code}`",
                               parse_mode="Markdown", reply_markup=markup)

                bot.send_message(ADMIN_CHAT_ID, f"📥 Pedido de {quantidade} créditos de @{call.from_user.username}")
            else:
                bot.send_message(call.message.chat.id, "❌ Erro ao gerar pagamento PIX.")

    def receber_mac(msg: Message):
        mac = msg.text
        pagamento = gerar_pagamento_pix("Mega IPTV", 65.00, msg.chat.id)

        if pagamento:
            pix_code = pagamento["pix_code"]
            qr_base64 = pagamento["qr_image"]
            with open("temp_qr.png", "wb") as f:
                f.write(base64.b64decode(qr_base64))

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("✅ Copiar Código PIX", switch_inline_query=pix_code))

            bot.send_photo(msg.chat.id, photo=open("temp_qr.png", "rb"),
                           caption=f"💳 *PIX Copia e Cola:*\n\n`{pix_code}`",
                           parse_mode="Markdown", reply_markup=markup)

            bot.send_message(ADMIN_CHAT_ID, f"📥 Pedido de IPTV\nMAC: {mac}\nCliente: @{msg.from_user.username}")
        else:
            bot.send_message(msg.chat.id, "❌ Erro ao gerar pagamento PIX.")
