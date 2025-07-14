import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PAWAN_API_KEY = os.environ.get("PAWAN_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

PAWAN_API_URL = "https://api.pawan.krd/chat/completions"

@app.route('/api/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if "message" not in data:
        return "no message", 200

    chat_id = data["message"]["chat"]["id"]
    user_msg = data["message"].get("text", "")

    if not user_msg:
        return "no text", 200

    # So‘rovni Pawan AI ga yuborish
    response = requests.post(PAWAN_API_URL, headers={
        "Authorization": f"Bearer {PAWAN_API_KEY}",
        "Content-Type": "application/json"
    }, json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_msg}]
    })

    if response.status_code == 200:
        reply_text = response.json()["choices"][0]["message"]["content"]
    else:
        reply_text = "AI javob bera olmadi. Keyinroq urinib ko‘ring."

    # Telegramga javob yuborish
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply_text
    })

    return "ok", 200
