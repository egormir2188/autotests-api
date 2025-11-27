from telegram import Bot
import asyncio

from tools.allure.formating_message import parse_allure_report, format_telegram_message
from config import BotConfig


passed, failed, broken,failed_tests = parse_allure_report('allure-report')
message = format_telegram_message(passed, failed, broken, failed_tests)

async def send_telegram_message_async():
    bot = Bot(token=BotConfig.bot_token)
    await bot.send_message(chat_id=BotConfig.chat_id, text=message, parse_mode='Markdown')

asyncio.run(send_telegram_message_async())