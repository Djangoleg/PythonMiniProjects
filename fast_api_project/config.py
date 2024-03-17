import os
import json
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

TIME_ZONE = "Europe/Moscow"

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

APP_LOGGER_NAME = 'currency'

# Currency.
CURRENCYLAYER_URL = os.getenv("CURRENCYLAYER_URL")
CURRENCYLAYER_API_KEY = os.getenv("CURRENCYLAYER_API_KEY")
CURRENCYLAYER_LIVE_URL = CURRENCYLAYER_URL + CURRENCYLAYER_API_KEY
CURRENCYLAYER_MASTER_CURRENCY = "USD"

CBRF_DAILY_URL = os.getenv("CBRF_DAILY_URL")

CURRENCY_PLOT_COLORS = {"USD": "green", "EUR": "red"}
CURRENCY_PLOT = ["USD", "EUR"]
NUMBER_DAY_FOR_PLOT = 3

# Celery.
CELERY_BROKER_URL = "redis://localhost:6379/11"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Every day at 3AM o'clock.
RUN_UPDATE_CURRENCY_RATE_TASK_CRONE = crontab(minute="*")
# RUN_UPDATE_CURRENCY_RATE_TASK_CRONE = crontab(minute="0", hour="3")
