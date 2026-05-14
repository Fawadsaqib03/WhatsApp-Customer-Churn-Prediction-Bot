import joblib
import numpy as np
from flask import Flask, request, make_response
from twilio.twiml.messaging_response import MessagingResponse
from preprocessing import parse_features

app = Flask(__name__)

# Load model and scaler
model  = joblib.load("artifacts/model.pkl")
scaler = joblib.load("artifacts/scaler.pkl")

# Churn class labels
CLASS_NAMES = {0: "Not Churned (Stay) ✅", 1: "Churned (Will Leave) ⚠️"}
EXPECTED_FEATURES = 11  # 11 features after encoding

# ── Health-check route (useful to verify ngrok is working) ──
@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is running! Send POST to /whatsapp"

# ── Main WhatsApp webhook ──
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.form.get("Body", "").strip()
    sender   = request.form.get("From", "")
    print(f"[IN] {sender}: {incoming}")

    resp = MessagingResponse()

    try:
        features = parse_features(incoming, EXPECTED_FEATURES)
    except ValueError as e:
        resp.message(
            f"❌ Error: {e}\n\n"
            f"Send 11 numbers in this order:\n"
            f"CreditScore, Age, Tenure, Balance, NumOfProducts, "
            f"HasCrCard, IsActiveMember, EstimatedSalary, "
            f"IsGermany(0/1), IsSpain(0/1), IsMale(0/1)\n\n"
            f"Example:\n619, 42, 2, 0.0, 1, 1, 1, 101348.88, 0, 0, 0"
        )
        twiml = str(resp)
        print(f"[OUT-XML] {twiml}")
        response = make_response(twiml)
        response.headers['Content-Type'] = 'text/xml'
        return response

    # Scale and predict
    X        = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)
    pred     = int(model.predict(X_scaled)[0])
    proba    = model.predict_proba(X_scaled)[0]
    conf     = float(proba.max())
    label    = CLASS_NAMES[pred]

    answer = (
        f"🏦 Customer Churn Prediction\n"
        f"──────────────────\n"
        f"Result: {label}\n"
        f"Confidence: {conf:.2%}"
    )
    print(f"[OUT] {answer}")
    resp.message(answer)

    twiml = str(resp)
    print(f"[OUT-XML] {twiml}")
    response = make_response(twiml)
    response.headers['Content-Type'] = 'text/xml'
    return response

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Flask server starting on http://0.0.0.0:5000")
    print("   Webhook endpoint: POST /whatsapp")
    print("   Health check:     GET  /")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)