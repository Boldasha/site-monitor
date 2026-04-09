import requests
import time
import logging
from datetime import datetime

BOT_TOKEN      = "8676870190:AAFDlaES0tIQgTbqZojyyOQP78W-0Qhcwio"
CHAT_ID        = "-2967692731"
SITE_URL       = "https://trs-dutyfree.ru/"
CHECK_INTERVAL = 60  # секунды между проверками

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        logging.error(f"Ошибка отправки в Telegram: {e}")

def check_site():
    try:
        r = requests.get(SITE_URL, timeout=10)
        return r.status_code < 500
    except Exception:
        return False

def main():
    logging.info(f"Мониторинг запущен: {SITE_URL}")
    site_up = True

    while True:
        is_up = check_site()
        now = datetime.now().strftime("%d.%m.%Y %H:%M")

        if not is_up and site_up:
            msg = (
                f"🔴 САЙТ НЕДОСТУПЕН!\n"
                f"🌐 {SITE_URL}\n"
                f"🕐 {now}\n"
                f"Проверьте хостинг или сервер."
            )
            send_telegram(msg)
            logging.warning("Сайт недоступен — уведомление отправлено")
            site_up = False

        elif is_up and not site_up:
            msg = (
                f"🟢 Сайт снова работает!\n"
                f"🌐 {SITE_URL}\n"
                f"🕐 {now}"
            )
            send_telegram(msg)
            logging.info("Сайт восстановлен — уведомление отправлено")
            site_up = True

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
