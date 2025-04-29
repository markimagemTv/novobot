from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.config import ADMIN_CHAT_ID
from app.mercado_pago import gerar_link_pagamento

def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(msg: Message):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Comprar Mega IPTV", callback_data="comprar_iptv"))
        markup.add(InlineKeyboardButton("Comprar Créditos Fast Play", callback_data="comprar_creditos"))
        bot.send_message(msg.chat.id, "Bem-vindo! Escolha uma opção:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        if call.data == "comprar_iptv":
            bot.send_message(call.message.chat.id, "Informe o MAC Address:")
            bot.register_next_step_handler(call.message, receber_mac)

    def receber_mac(msg: Message):
        mac = msg.text.strip().upper()

        # Validação simples de MAC (opcional)
        if not (len(mac) == 17 and all(c in "0123456789ABCDEF:-" for c in mac.upper())):
            bot.send_message(msg.chat.id, "❌ MAC Address inválido. Tente novamente.")
            return

        try:
            link_pagamento = gerar_link_pagamento("Mega IPTV", 65.00, msg.chat.id)
            bot.send_message(msg.chat.id, f"💳 Clique para pagar via Mercado Pago:\n{link_pagamento}")

            cliente = f"@{msg.from_user.username}" if msg.from_user.username else f"ID: {msg.from_user.id}"
            bot.send_message(ADMIN_CHAT_ID, f"📥 Novo pedido de IPTV\nMAC: {mac}\nCliente: {cliente}")
        except Exception as e:
            bot.send_message(msg.chat.id, "❌ Erro ao gerar link de pagamento.")
            print(f"[Erro gerar MAC] {e}")
