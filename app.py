from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ tracking imports
import requests
import socket
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# =========================
# 🧠 LOAD ML MODEL
# =========================
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# =========================
# 🌍 IMPROVED GEO TRACKING
# =========================
def get_geo_info(url):
    try:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        domain = parsed.netloc if parsed.netloc else parsed.path
        domain = domain.split(":")[0]

        # 🚫 handle localhost
        if domain in ["127.0.0.1", "localhost", ""]:
            return {
                "ip": "Localhost",
                "country": "Local",
                "city": "Local",
                "lat": 0,
                "lon": 0
            }

        # =========================
        # METHOD 1: DOMAIN → IP
        # =========================
        try:
            ip = socket.gethostbyname(domain)
        except:
            ip = None

        # =========================
        # METHOD 2: PUBLIC IP FALLBACK
        # =========================
        if not ip or ip == "0.0.0.0":
            ip = requests.get("https://api.ipify.org", timeout=5).text

        # =========================
        # METHOD 3: GEO API
        # =========================
        geo = requests.get(
            f"http://ip-api.com/json/{ip}",
            timeout=5
        ).json()

        return {
            "ip": ip,
            "country": geo.get("country", "Unknown"),
            "city": geo.get("city", "Unknown"),
            "lat": geo.get("lat", 0),
            "lon": geo.get("lon", 0)
        }

    except Exception as e:
        print("Geo error:", e)

        # FINAL FALLBACK
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()

            return {
                "ip": ip,
                "country": geo.get("country", "Unknown"),
                "city": geo.get("city", "Unknown"),
                "lat": geo.get("lat", 0),
                "lon": geo.get("lon", 0)
            }
        except:
            return {
                "ip": "Unknown",
                "country": "Unknown",
                "city": "Unknown",
                "lat": 0,
                "lon": 0
            }

# =========================
# 📧 EMAIL ALERT (UNCHANGED)
# =========================
def send_email_alert(url, risk):
    print("📧 Trying to send email...")

    try:
        sender_email = "mansimajukar538@gmail.com"
        sender_password = "hbquonocwjsggqmc"
        receiver_email = "mansimajukar538@gmail.com"

        subject = "Phishing Alert Detected"

        body = f"""Phishing URL Detected!

URL: {url}
Risk Score: {risk}%
Time: {datetime.now()}
"""

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email failed:", e)


# =========================
# 🧠 HOME ROUTE
# =========================
@app.route("/")
def home():
    return "ML Backend Running"


# =========================
# 🧪 TEST EMAIL ROUTE
# =========================
@app.route("/test-email")
def test_email():
    send_email_alert("http://test-phishing.com", 99)
    return "Test email triggered"


# =========================
# 🔍 PREDICT ROUTE
# =========================
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(force=True)
    url = data.get("url", "").strip().lower()

    if not url:
        return jsonify({
            "prediction": "Invalid",
            "risk_score": 0,
            "url": url,
            "time": str(datetime.now())
        })

    # ML prediction
    vec = vectorizer.transform([url])
    result = model.predict(vec)[0]

    try:
        prob = model.predict_proba(vec)[0]
        risk = int(max(prob) * 100)
    except:
        risk = 70

    prediction = "Phishing" if result.lower() == "phishing" else "Safe"

    # 🌍 GET GEO DATA
    geo = get_geo_info(url)

    # 🚨 EMAIL ALERT
    if prediction == "Phishing":
        print("🚨 Alert Phishing detected! Sending alert...")
        send_email_alert(url, risk)

    return jsonify({
        "prediction": prediction,
        "risk_score": risk,
        "url": url,
        "time": str(datetime.now()),

        # ✅ GEO DATA
        "ip": geo["ip"],
        "country": geo["country"],
        "city": geo["city"],
        "lat": geo["lat"],
        "lon": geo["lon"]
    })


# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    print("🌍 ML Backend + Tracking Running at http://127.0.0.1:5000")
    app.run(debug=True)