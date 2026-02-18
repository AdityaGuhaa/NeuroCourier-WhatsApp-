import requests
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import ollama

app = FastAPI()

# ===== CONFIG =====

VERIFY_TOKEN = "Put Your Verify Token Here"

ACCESS_TOKEN = "Put Your Access Token Here"
PHONE_NUMBER_ID = "Put Your Phone Number ID Here"

MODEL_NAME = "qwen3-vl:2b"


# ===== SEND MESSAGE FUNCTION =====

def send_whatsapp_message(to: str, text: str):

    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        print("WhatsApp API response:", response.status_code, response.text)

    except Exception as e:
        print("Send message error:", e)


# ===== OLLAMA REPLY FUNCTION =====

def generate_reply(user_message: str) -> str:

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are NeuroCourier, a helpful AI assistant created by Aditya Guha. Be helpful, concise, and intelligent."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply = response["message"]["content"]

        return reply

    except Exception as e:

        print("Ollama error:", e)

        return "Sorry, I encountered an error while processing your request."


# ===== WEBHOOK VERIFICATION (REQUIRED BY META) =====

@app.get("/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:

        print("Webhook verified successfully")

        return PlainTextResponse(content=challenge)

    return PlainTextResponse(content="Verification failed", status_code=403)


# ===== RECEIVE MESSAGE WEBHOOK =====

@app.post("/webhook")
async def webhook(request: Request):

    try:

        data = await request.json()

        print("\n===== FULL WEBHOOK RECEIVED =====")
        print(data)
        print("=================================\n")

        if "entry" not in data:
            return {"status": "no entry"}

        for entry in data["entry"]:

            for change in entry.get("changes", []):

                value = change.get("value", {})

                # Ignore events without messages
                if "messages" not in value:
                    continue

                for message in value["messages"]:

                    sender = message.get("from")

                    # Only handle text messages
                    if message.get("type") != "text":
                        print("Non-text message received, ignoring.")
                        continue

                    user_text = message["text"]["body"]

                    print(f"Message from {sender}: {user_text}")

                    # Generate AI reply
                    reply = generate_reply(user_text)

                    print(f"Reply to {sender}: {reply}")

                    # Send reply
                    send_whatsapp_message(sender, reply)

        return {"status": "ok"}

    except Exception as e:

        print("Webhook processing error:", e)

        return {"status": "error"}
