import os
import json
from pathlib import Path

from dotenv import load_dotenv

TIME_ZONE = "Europe/Moscow"

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

APP_LOGGER_NAME = 'currency'
NOTIFY_DATE_TIME_PATTERN = '%d.%m.%Y %H:%M:%S'

# Telegram settings.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_IDS = json.loads(os.getenv("TELEGRAM_CHAT_IDS"))

# Currency.
CURRENCYLAYER_URL = os.getenv("CURRENCYLAYER_URL")
CURRENCYLAYER_API_KEY = os.getenv("CURRENCYLAYER_API_KEY")
CURRENCYLAYER_LIVE_URL = CURRENCYLAYER_URL + CURRENCYLAYER_API_KEY
CURRENCYLAYER_MASTER_CURRENCY = "USD"

CBRF_DAILY_URL = os.getenv("CBRF_DAILY_URL")

CURRENCY_PLOT_COLORS = {"USD": "green", "EUR": "red"}
CURRENCY_PLOT = ["USD", "EUR"]
CURRENCY_PLOT_FILE_PATH = "media/plot/"
