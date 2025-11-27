import httpx

from config import BotConfig


def send_telegram_message(message: str):
    url = f'{BotConfig.telegram_host}/{BotConfig.send_message_uri}'
    payload = {"chat_id": BotConfig.chat_id, "text": message}

    httpx.post(url, data=payload)