import smtplib
from email.mime.text import MIMEText

def send_email_alert(url):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    receiver = "admin@gmail.com"

    message = MIMEText(f"⚠ Phishing URL detected: {url}")
    message["Subject"] = "Phishing Detection Alert"
    message["From"] = sender
    message["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
        server.quit()

        print("Email Alert Sent Successfully")

    except Exception as e:
        print("Email Error:", e)