from flask import Flask, request
import requests
import json

app = Flask(__name__)

ACCESS_TOKEN = "EAFU91yTp844BPNSSXNTtzPvhsFvYL33nm8xON7Si3QcCisTUlsamSIrZBZAa28JRVVoGyVilGc31hBcs9HZBfw87ZC1mZBTqN30JNwe2ZCKICB1upUh35433ov4hX7q1yZAMPRMl7psYBVt8jsUJMpFNspNr2hu6OFkz4bNRuYbFbQtfMklOINy8PRI7CLCKyoYAZC4aVZBWadMoByrmXGteISgZCO4HGjs88xcK44BTm4PP0MNerLDAZBaJMW5FlYuggZDZD"
PHONE_NUMBER_ID = "739888019204601"
VERIFY_TOKEN = "vtu_verify_token"

# 🧠 In-memory transaction history (user_id -> list of actions)
user_history = {}

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token"

    if request.method == "POST":
        data = request.get_json()
        print("Incoming message:", json.dumps(data, indent=2))

        try:
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            messages = value.get("messages")

            if messages:
                for message in messages:
                    sender = message["from"]
                    text = message["text"]["body"].strip().lower()

                    # Initialize history for user if not present
                    if sender not in user_history:
                        user_history[sender] = []

                    if text in ["hi", "hello"]:
                        send_message(sender, f"""👋 Hello, welcome to Fast VTU Bot!

Reply with:
1. Buy Data 📶
2. Buy Airtime 💳
3. Top Up Wallet 💰
4. My Balance 📂
5. NEPA Bill ⚡
6. Cable Subscription 📺
7. My Transaction History 📜
""")
                    elif text == "1":
                        record_action(sender, "Bought Data")
                        send_message(sender, "✅ You selected *Buy Data*. (Feature coming soon)")
                    elif text == "2":
                        record_action(sender, "Bought Airtime")
                        send_message(sender, "✅ You selected *Buy Airtime*. (Feature coming soon)")
                    elif text == "3":
                        record_action(sender, "Topped Up Wallet")
                        send_message(sender, "✅ You selected *Top Up Wallet*. (Feature coming soon)")
                    elif text == "4":
                        send_message(sender, "💼 Your balance is ₦0 (Wallet feature coming soon)")
                    elif text == "5":
                        record_action(sender, "Paid NEPA Bill")
                        send_message(sender, "✅ You selected *NEPA Bill*. (Feature coming soon)")
                    elif text == "6":
                        record_action(sender, "Subscribed to Cable")
                        send_message(sender, "✅ You selected *Cable Subscription*. (Feature coming soon)")
                    elif text == "7" or "history" in text:
                        show_history(sender)
                    else:
                        send_message(sender, "❗ Please type *Hi* to see options or choose a valid number (1-7)")

        except Exception as e:
            print("Error:", e)

        return "ok", 200

def record_action(user_id, action):
    user_history[user_id].append(action)

def show_history(user_id):
    history = user_history.get(user_id, [])
    if not history:
        send_message(user_id, "📜 You have no transaction history yet.")
    else:
        lines = "\n".join([f"{i+1}. {item}" for i, item in enumerate(history)])
        send_message(user_id, f"📜 *Your Transaction History:*\n{lines}")

def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Message send response:", response.text)

if __name__ == "__main__":
    app.run()
