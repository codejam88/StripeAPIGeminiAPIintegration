import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import stripe
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize API Keys from your .env file
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Enable CORS so your frontend can talk to your backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Serve the frontend UI
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("index.html", "r") as f:
        return f.read()

# 2. Endpoint to create the Stripe Checkout Page
@app.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    try:
        body = await request.json()
        user_prompt = body.get("prompt", "Write a short poem about coding.")

        # We pass the user's prompt into the metadata so Stripe holds onto it 
        # and sends it back to us in the webhook once payment succeeds.
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Premium AI Generation Credit',
                        'description': f'Trigger prompt: "{user_prompt}"',
                    },
                    'unit_amount': 100,  # $1.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            metadata={'user_prompt': user_prompt},
            success_url='http://localhost:8000/?status=success',
            cancel_url='http://localhost:8000/?status=cancel',
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3. The Webhook Receiver: Listens for Stripe payment confirmations
@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        # Verify that the event actually came from Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the successful payment event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Crash-proof extraction using bracket lookups supported by the Stripe SDK
        saved_prompt = "Write a short poem about coding."
        if "metadata" in session and session["metadata"]:
            if "user_prompt" in session["metadata"]:
                saved_prompt = session["metadata"]["user_prompt"]
        
        print(f"💰 Payment successful! Processing prompt: {saved_prompt}")

# Call Gemini to generate the premium response
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=(
                    f"The user paid $1 to unlock a premium generation. "
                    f"Write a beautiful, creative Haiku (strictly follow the 5-7-5 syllable structure) "
                    f"based exactly on this topic: {saved_prompt}. "
                    f"Return ONLY the haiku lines, nothing else."
                )
            )
            ai_result = response.text
            
            # Bright Green color code wrapper
            GREEN = "\033[92m"
            RESET = "\033[0m"

            print(f"\n{GREEN}🤖 === GEMINI PREMIUM GENERATION === 🤖")
            print(ai_result)
            print(f"========================================{RESET}\n")
            
        except Exception as e:
            print(f"Failed to generate AI content: {e}")

    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)