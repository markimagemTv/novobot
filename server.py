from flask import Flask, request, render_template
from app.bot import bot
import threading

app = Flask(__name__)

@app.route("/")
def index():
    # Aqui seria seu dashboard
    return render_template("dashboard.html", vendas=[])

@app.route("/pagamento/webhook", methods=["POST"])
def pagamento_webhook():
    data = request.json
    if data and data.get("action") == "payment.created":
        # Você pode consultar o pagamento com o ID
        print("Novo pagamento recebido!", data)
    return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=bot.run_bot).start()
    app.run(host="0.0.0.0", port=5000)
