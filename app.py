from flask import Flask, request
import requests

app = Flask(__name__)

# Replace this with your own verify token
VERIFY_TOKEN = "vtu_verify_token"

# Your real credentials from Meta
ACCESS_TOKEN = "EAFU91yTp844BPOn0JbkWLmTnrcGOIZBGP7gAGHkQJUZBodbPUYLywaZAE5eK5Rhq7PHH9lHnWZBdbm7HTvDVQ7PZBV6cbEvPaK7dwRAhaKLLMF9usrIl4I9ltMBC4TcstzZBYU5KeIu7dkKvUtwA2fHJ7xUXJxxB4kRb34U0U1ZAd7ZBJBwBeiZBeGfvEd2xBb7O8jDXrocED2FI7jofYeIVvQYhZBZBGPERDGRrd42oCs2Ik6CoQ6qZCF73wlRuA6TuIgZDZD"
PHONE_NUMBER_ID = "739888019204601"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification from Meta
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verify token", 403

    if request.method == 'POST':
        data = request.get_json()
        try:
            # Extract message and sender number
            msg = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'].lower()
            sender = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            handle_message(sender, msg)
        except:
            pass
        return "ok", 200

def handle_message(sender, msg):
    if msg in ["hi", "hello", "menu"]:
        response = (
            "👋 *Welcome to Fast VTU Bot!*\nReply with:\n"
            "1. Buy Data 📶\n"
            "2. Buy Airtime 💳\n"
            "3. Top Up Wallet 💰\n"
            "4. My Balance 📂\n"
            "5. Cable Subscription 📺\n"
            "6. NEPA Bill ⚡"
        )
    else:
        response = "❌ Invalid input. Please reply with a number from 1 to 6."
    
    send_message(sender, response)

def send_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(port=5000)
