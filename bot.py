import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

def test():
    now = datetime.utcnow().strftime("%d/%m/%Y — %H:%M UTC")
    text = f"✅ <b>رسالة اختبار</b>\n🕐 {now}\n\nالبوت يعمل بشكل صحيح!"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    r = requests.post(url, json=payload, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")

if __name__ == "__main__":
    test()
