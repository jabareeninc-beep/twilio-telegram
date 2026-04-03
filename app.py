import os
import requests
from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]

@app.route("/sms", methods=["POST"])
def sms_incoming():
    from_number = request.form.get("From")
    body = request.form.get("Body")
    msg = f"📩 From {from_number}:\n{body}"
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    )
    return '<?xml version="1.0" encoding="UTF-8"?><Response></Response>', 200

@app.route("/telegram", methods=["POST"])
def telegram_incoming():
    data = request.json
    text = data["message"]["text"]
    if ":" in text:
        to_number, body = text.split(":", 1)
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=body.strip(),
            from_=TWILIO_PHONE_NUMBER,
            to=to_number.strip()
        )
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
