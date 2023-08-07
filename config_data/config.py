import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_API = os.getenv("SITE_API")

DEFAULT_COMMANDS = (
    ("start", "Запуск бота"),
    ("help", "получить список всех доступных команд."),
    ("hello_world", "Тестовый вывод"),
    ("low", "Поиск ближайшего аэропорта по геолокации"),
    ("high", "Поиск аэропортов в выбранном городе"),
    ("custom", "Получение данных о прошедшем/текущем/будущем рейсе"),
    ("history", "История поисков"),
)

class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("SITE_API", None)
    host_api: StrictStr = os.getenv("HOST_API", None)
