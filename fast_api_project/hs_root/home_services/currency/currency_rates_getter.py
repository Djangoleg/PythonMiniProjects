import logging

import requests
from requests import HTTPError, Timeout, RequestException

from config import (
    APP_LOGGER_NAME,
    CURRENCYLAYER_LIVE_URL,
    CBRF_DAILY_URL,
    CURRENCYLAYER_MASTER_CURRENCY,
)

app_logger = logging.getLogger(APP_LOGGER_NAME)


async def get_exchange_rates_currencylayer(currencies: list, target: str) -> dict:
    request = None
    cur_val = dict()

    try:
        if len(currencies) == 0:
            message = "Get exchange rates from Currencylayer. Currency list is empty"
            app_logger.error(message)
            raise Exception(
                message
            )

        if len(target) == 0:
            message = "Get exchange rates from Currencylayer. Target value is empty"
            app_logger.error(message)
            raise Exception(
                message
            )

        url = f"{CURRENCYLAYER_LIVE_URL}" f'&currencies={",".join(currencies)}'

        app_logger.info(f"Currencylayer request: {url}")

        request = requests.get(url)
        request.raise_for_status()
        data = request.json()

        app_logger.info(f"Currencylayer response: {data}")

        quotes = dict()

        if data.get("success"):
            success = data.get("success")
            if success:
                if data.get("quotes"):
                    quotes = data.get("quotes")
            else:
                if data.get("error"):
                    error = data.get("error")
                    if error.get("code") and error.get("info"):
                        code = error.get("code")
                        info = error.get("info")
                        message = f"Code: {code}, Info: {info}"
                        app_logger.error(message)
                        raise Exception(message)

        # Conversion to the desired target currency. Maybe this should be moved out.
        master_val = 0.0
        if quotes.get(f"{CURRENCYLAYER_MASTER_CURRENCY}{target}"):
            master_val = quotes.get(f"{CURRENCYLAYER_MASTER_CURRENCY}{target}")

        if len(quotes.items()) > 0:
            for currency in currencies:
                if currency != CURRENCYLAYER_MASTER_CURRENCY:
                    if currency == target:
                        cur_val[CURRENCYLAYER_MASTER_CURRENCY] = round(master_val, 4)
                    else:
                        if quotes.get(f"{CURRENCYLAYER_MASTER_CURRENCY}{currency}"):
                            cur_val[currency] = round(
                                master_val
                                / quotes.get(
                                    f"{CURRENCYLAYER_MASTER_CURRENCY}{currency}"
                                ),
                                4,
                            )

        return cur_val

    except HTTPError as e:
        app_logger.error(f"Http Error: {e} Text: {request.text}")
        cur_val["error"] = e.strerror
        return cur_val
    except ConnectionError as e:
        app_logger.error(f"Error Connecting: {e} Text: {request.text}")
        cur_val["error"] = e.strerror
        return cur_val
    except Timeout as e:
        app_logger.error(f"Timeout Error: {e} {request.text}")
        cur_val["error"] = e.strerror
        return cur_val
    except RequestException as e:
        app_logger.error(f"OOps: Something Else: {e} Text: {request.text}")
        cur_val["error"] = e.strerror
        return cur_val
    except Exception as e:
        app_logger.error(f"Error getting exchange rates: {e} Text: {request.text}")
        if hasattr(e, "message"):
            cur_val["error"] = e.message
        else:
            cur_val["error"] = str(e)
        return cur_val


async def get_exchange_rates_cbrf(currencies: list, target: str = None) -> dict:
    """
    TODO: Engage target currency.
    """
    app_logger.info(f"Cbrf request: {CBRF_DAILY_URL}")
    quotes = dict()
    currency_values = dict()

    if len(currencies) == 0:
        raise Exception("Get exchange rates from CBRF. Currency list is empty")

    try:
        request = requests.get(CBRF_DAILY_URL)
        request.raise_for_status()
        data = request.json()

        app_logger.info(f"Cbrf response: {data}")

        if data.get("Valute"):
            currency_values = data.get("Valute")

        if len(currency_values.items()) > 0:
            for currency in currencies:
                if currency_values.get(currency):
                    tmp_dict = currency_values.get(currency)
                    nominal = 1
                    value = 0
                    if tmp_dict.get("Value"):
                        value = float(tmp_dict.get("Value"))
                    if tmp_dict.get("Nominal"):
                        nominal = float(tmp_dict.get("Nominal"))

                    quotes[currency] = round(value / nominal, 4)

        return quotes

    except HTTPError as e:
        app_logger.error(f"Http Error: {e} Text: {e.request}")
        quotes["error"] = e.strerror
        return quotes
    except ConnectionError as e:
        app_logger.error(f"Error Connecting: {e}")
        quotes["error"] = e.strerror
        return quotes
    except Timeout as e:
        app_logger.error(f"Timeout Error: {e}")
        quotes["error"] = e.strerror
        return quotes
    except RequestException as e:
        app_logger.error(f"OOps: Something Else: {e} Text: {e.request}")
        quotes["error"] = e.strerror
        return quotes
    except Exception as e:
        app_logger.error(f"Error getting exchange rates: {e}")
        if hasattr(e, "message"):
            quotes["error"] = e.message
        else:
            quotes["error"] = str(e)
        return quotes
