from datetime import datetime
from typing import Tuple

import logger
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import pytz

from config import APP_LOGGER_NAME, TIME_ZONE
from .crud import get_currency_provider, get_currency, create_currency_rate as db_create_currency_rate
from .currency_rates_getter import get_exchange_rates_currencylayer, get_exchange_rates_cbrf
from .database import SessionLocal
from .schemas import CurrencyRateRequestData, CurrencyRateCreate

app_logger = logging.getLogger(APP_LOGGER_NAME)

app = FastAPI()


def get_db():
    """
    Get database
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_currency_rate_string(
        rate_result: dict, currency_source: list, source: str
) -> str:
    """
    Result string formation.
    """
    if not rate_result:
        return str()

    result = f"✅ <b>{source.upper()}</b>:\n"

    for curr in sorted(currency_source):
        if curr in rate_result:
            result += f"{curr.upper()}: {rate_result[curr]}\n"

    return result


def create_currency_rate(db: Session, currencylayer: dict, cbrf: dict, target: str) -> None:
    """
    Create CurrencyRate records.
    """
    try:
        provider_currency_layer = get_currency_provider(db=db, name="Currencylayer")
        provider_cbrf = get_currency_provider(db=db, name="CBRF")
        date = datetime.now(tz=pytz.timezone(TIME_ZONE))

        currency_target = get_currency(db=db, name=target)

        for key, value in currencylayer.items():
            currency = get_currency(db=db, name=key)
            if currency:

                crc = CurrencyRateCreate()
                crc.request_date = date
                crc.currency = currency.id
                crc.provider = provider_currency_layer.id
                crc.master_currency = currency_target.id
                crc.amount = value

                db_create_currency_rate(db=db, cr=crc)

        for key, value in cbrf.items():
            currency = get_currency(db=db, name=key)
            if currency:

                crc = CurrencyRateCreate()
                crc.request_date = date
                crc.currency = currency.id
                crc.provider = provider_cbrf.id
                crc.master_currency = currency_target.id
                crc.amount = value

                db_create_currency_rate(db=db, cr=crc)

    except Exception as e:
        app_logger.error(f"Error create CurrencyRate records: {e}")


def get_exchange_rate_data(source: list, target: str) -> tuple[dict, dict]:
    """
    Get currency exchange rate.
    """
    source.append(target)

    # Get from Currencylayer.
    currencylayer = get_exchange_rates_currencylayer(
        currencies=source, target=target
    )

    # Get from CBRF.
    cbrf = get_exchange_rates_cbrf(currencies=source)

    return currencylayer, cbrf


@app.get("/currency/rate/")
async def get_currency_rate(db: Session = Depends(get_db), data: CurrencyRateRequestData = None):
    if data is None:
        error_message = "Request data is empty"
        app_logger.error(error_message)
        raise HTTPException(status_code=404, detail=error_message)

    if data.currency_target is None or not data.currency_target:
        error_message = "Field currency_target is empty"
        app_logger.error(error_message)
        raise HTTPException(status_code=404, detail=error_message)

    if data.currencies_source is None or not data.currencies_source:
        error_message = "Field currencies_source is empty"
        app_logger.error(error_message)
        raise HTTPException(status_code=404, detail=error_message)

    app_logger.info(data)

    source = data.currencies_source
    target = data.currencies_target

    er_data = get_exchange_rate_data(source, target)

    # Save data.
    create_currency_rate(db=db, currencylayer=er_data[0], cbrf=er_data[1], target=target)

    response = {
        "data": f"{get_currency_rate_string(er_data[1], source, "cbrf")}\n"
                f"{get_currency_rate_string(er_data[0], source, "currencylayer")}"
    }

    return response
