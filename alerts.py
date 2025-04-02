import smtplib
from email.message import EmailMessage
import logging

logging.basicConfig(filename='alerts.log', level=logging.INFO)

# Email Configuration
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"

def send_email_alert(anomaly_count):
    msg = EmailMessage()
    msg['Subject'] = "🚨 API Anomaly Detected!"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = "recipient@example.com"
    msg.set_content(f"{anomaly_count} anomalies detected in the API system. Please check the logs.")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    
    logging.info(f"Sent alert: {anomaly_count} anomalies detected.")

if __name__ == "__main__":
    send_email_alert(3)
