import hashlib
import secrets
from typing import Annotated

from starlette.responses import StreamingResponse

import logger
import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from config import APP_LOGGER_NAME
from currency.crud import get_user

from currency.database import get_db
from currency.get_currency_rate_helper import get_exchange_rate_data, create_currency_rate, get_currency_rate_string
from currency.plot_helper import get_currency_rates_data, generate_plot
from currency.schemas import CurrencyRateRequestData

app_logger = logging.getLogger(APP_LOGGER_NAME)

app = FastAPI()
security = HTTPBasic()


def check_credentials(
        db: Session = Depends(get_db),
        credentials: Annotated[HTTPBasicCredentials, Depends(security)] = None,
):
    """
    Check if credentials are.
    :param db:
    :param credentials:
    :return:
    """
    if not credentials:
        return False

    user = get_user(db, credentials.username)

    if not user:
        return False

    current_password_hash = hashlib.sha256(credentials.password.encode("utf8")).hexdigest()
    is_correct_password = secrets.compare_digest(current_password_hash, user.password.decode("utf8"))
    if not is_correct_password:
        return False

    return True


@app.get("/currency/rate/")
async def get_currency_rate(db: Session = Depends(get_db),
                            is_auth: bool = Depends(check_credentials),
                            data: CurrencyRateRequestData = None):
    """
    Get currency rate.
    :param is_auth:
    :param db:
    :param data:
    :return:
    """
    if not is_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

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

    er_data = await get_exchange_rate_data(source, target)

    # Save data.
    create_currency_rate(db=db, currencylayer=er_data[0], cbrf=er_data[1], target=target)

    response = {
        "data": f"{get_currency_rate_string(er_data[1], source, "cbrf")}\n"
                f"{get_currency_rate_string(er_data[0], source, "currencylayer")}"
    }

    app_logger.info(f"Response: {response}")

    return response


@app.get("/currency/plot/")
async def get_currency_rates_plot(db: Session = Depends(get_db), is_auth: bool = Depends(check_credentials)):
    """
    Get currency rates plot.
    """
    if not is_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    app_logger.info(f"A request to generate a chart was received")

    currency_rates_data = get_currency_rates_data(db)
    buf = generate_plot(currency_rates_data)
    if buf is None:
        error_message = "No data for the graph"
        app_logger.error(error_message)
        raise HTTPException(status_code=404, detail=error_message)

    app_logger.info(f"Response sent")

    return StreamingResponse(buf, media_type="image/jpeg")
