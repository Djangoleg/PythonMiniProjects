import asyncio
import logging

import logger
from celery_app import app
from config import APP_LOGGER_NAME
from currency.database import get_db
from currency.get_currency_rate_helper import get_exchange_rate_data, create_currency_rate

celery_logger = logging.getLogger(APP_LOGGER_NAME)


@app.task
def update_currency_rate_task():
    """
    Updates currency rate task.
    """
    celery_logger.info("Start updating currency rate task")
    currencies_source = ["USD", "EUR", "GBP", "UAH", "CNY"]
    currency_target = "RUB"
    try:

        generator = get_db()
        db = next(generator)

        er_data = asyncio.run(get_exchange_rate_data(currencies_source, currency_target))
        celery_logger.info(f"End updating currency rate task. Data: {er_data}")

        # Save data.
        create_currency_rate(db=db, currencylayer=er_data[0], cbrf=er_data[1], target=currency_target)

    except Exception as e:
        celery_logger.info(f"Error updating currency rate task: {e}")
