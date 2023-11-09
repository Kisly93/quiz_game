import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
TELEGRAM_BOT_API = os.getenv('TELEGRAM_BOT_API')
VK_TOKEN = os.getenv('VK_TOKEN')
