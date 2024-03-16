import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from config import APP_LOGGER_NAME
from .crud import get_currency_provider, get_currency, create_currency_rate as db_create_currency_rate
from .currency_rates_getter import get_exchange_rates_currencylayer, get_exchange_rates_cbrf

app_logger = logging.getLogger(APP_LOGGER_NAME)


def create_currency_rate(db: Session, currencylayer: dict, cbrf: dict, target: str) -> None:
    """
    Create CurrencyRate records.
    """
    try:
        provider_currency_layer = get_currency_provider(db=db, name="Currencylayer")
        provider_cbrf = get_currency_provider(db=db, name="CBRF")
        # date = datetime.now(tz=pytz.timezone(TIME_ZONE))
        date = datetime.now(tz=timezone.utc)

        currency_target = get_currency(db=db, name=target)

        for key, value in currencylayer.items():
            currency = get_currency(db=db, name=key)
            if currency:
                db_create_currency_rate(db=db, request_date=date, currency=currency,
                                        provider=provider_currency_layer,
                                        master_currency=currency_target, amount=value)

        for key, value in cbrf.items():
            currency = get_currency(db=db, name=key)
            if currency:
                db_create_currency_rate(db=db, request_date=date, currency=currency,
                                        provider=provider_cbrf,
                                        master_currency=currency_target, amount=value)

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
