import asyncio, shutil

from datetime import datetime
from telegram import Bot
from tools.allure.formating_message import parse_allure_report, format_telegram_message
from config import BotConfig


passed, failed, broken,failed_tests = parse_allure_report('allure-report')
message = format_telegram_message(passed, failed, broken, failed_tests)

current_time = datetime.now()
formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
file_name = f'allure-report_{formatted_time}'

shutil.make_archive(f'./bot/artifacts/{file_name}', 'zip', 'allure-report')

async def send_telegram_test_artifacts_async(file_path: str, caption: str):
    bot = Bot(token=BotConfig.bot_token)
    with open(file_path, 'rb') as file:
        await bot.send_document(chat_id=BotConfig.chat_id, document=file, caption=caption, parse_mode='Markdown')

def send_telegram_artifacts(file_path: str, caption: str):
    asyncio.run(send_telegram_test_artifacts_async(file_path, caption))


send_telegram_artifacts(f'bot/artifacts/{file_name}.zip', message)