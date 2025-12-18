import time
import requests

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8481023375:AAEJoWkaA4idW8sbh-mudbXi7cxQugViDCU"
CHANNEL_ID = "@akermannewss"

ALARM_STICKER = "CAACAgIAAxkBAAE_YMlpQuc81w1-Hhoc0O8wO34Uhvkv4gACSIgAAqP-SElRXa0dAduIuTYE"
CLEAR_STICKER = "CAACAgIAAxkBAAE_YMtpQudB0KIhjT-fkgl3EyssZg6JhgACOYcAAufjQUkaHrHN24tqKTYE"

CHECK_DELAY = 20
# =====================

TG = f"https://api.telegram.org/bot{BOT_TOKEN}"
API_URL = "https://alerts.in.ua/api/states"

last_state = None


def send_sticker(sticker):
    requests.post(
        f"{TG}/sendSticker",
        data={"chat_id": CHANNEL_ID, "sticker": sticker},
        timeout=15
    )


print("Бот запущен, слежу за Одесской областью")

while True:
    try:
        data = requests.get(API_URL, timeout=10).json()
        region = next(r for r in data["regions"] if r["id"] == "odesa")

        if region["alert"] and last_state != "alarm":
            send_sticker(ALARM_STICKER)
            last_state = "alarm"
            print("🚨 Тревога")

        if not region["alert"] and last_state != "clear":
            send_sticker(CLEAR_STICKER)
            last_state = "clear"
            print("✅ Отбой")

    except Exception as e:
        print("Ошибка:", e)

    time.sleep(CHECK_DELAY)
