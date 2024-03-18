from starlette.responses import StreamingResponse

import logger
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from config import APP_LOGGER_NAME

from .database import get_db
from .get_currency_rate_helper import get_exchange_rate_data, create_currency_rate, get_currency_rate_string
from .plot_helper import get_currency_rates_data, generate_plot
from .schemas import CurrencyRateRequestData

app_logger = logging.getLogger(APP_LOGGER_NAME)

app = FastAPI()


@app.get("/currency/rate/")
async def get_currency_rate(db: Session = Depends(get_db), data: CurrencyRateRequestData = None):
    """
    Get currency rate.
    :param db:
    :param data:
    :return:
    """
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
    target = data.currency_target

    er_data = get_exchange_rate_data(source, target)

    # Save data.
    create_currency_rate(db=db, currencylayer=er_data[0], cbrf=er_data[1], target=target)

    response = {
        "data": f"{get_currency_rate_string(er_data[1], source, "cbrf")}\n"
                f"{get_currency_rate_string(er_data[0], source, "currencylayer")}"
    }

    app_logger.info(f"Response: {response}")

    return response


@app.get("/currency/plot/")
async def get_currency_rates_plot(db: Session = Depends(get_db)):
    """
    Get currency rates plot.
    """
    app_logger.info(f"A request to generate a chart was received")

    currency_rates_data = get_currency_rates_data(db)
    buf = generate_plot(currency_rates_data)
    if buf is None:
        error_message = "No data for the graph"
        app_logger.error(error_message)
        raise HTTPException(status_code=404, detail=error_message)

    app_logger.info(f"Response sent")

    return StreamingResponse(buf, media_type="image/jpeg")
