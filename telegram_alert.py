import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("📱 Telegram alert sent!")
        else:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Telegram failed: {e}")

def send_opportunity_alert(triangle, profit, scan_count):
    message = (
        f"🚨 <b>ARB OPPORTUNITY FOUND!</b>\n\n"
        f"📊 Triangle: <code>{triangle}</code>\n"
        f"💰 Profit: <b>{profit*100:.4f}%</b>\n"
        f"🔢 Scan: #{scan_count}\n\n"
        f"⚡ Bot is executing trade now..."
    )
    send_alert(message)

def send_trade_result(triangle, profit_usdt, success):
    if success:
        message = (
            f"✅ <b>TRADE COMPLETE</b>\n\n"
            f"📊 Triangle: <code>{triangle}</code>\n"
            f"💵 Actual profit: <b>{profit_usdt:.4f} USDT</b>"
        )
    else:
        message = (
            f"❌ <b>TRADE FAILED</b>\n\n"
            f"📊 Triangle: <code>{triangle}</code>\n"
            f"⚠️ Check bot logs for details"
        )
    send_alert(message)

def send_startup_alert(triangle_count):
    message = (
        f"🤖 <b>Arb Bot Started!</b>\n\n"
        f"🔍 Scanning <b>{triangle_count}</b> triangles\n"
        f"⚡ WebSocket connected\n"
        f"👀 Watching for opportunities..."
    )
    send_alert(message)