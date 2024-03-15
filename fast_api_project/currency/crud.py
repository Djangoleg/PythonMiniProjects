from datetime import datetime

from sqlalchemy.orm import Session

from currency import models


def get_currency_provider(db: Session, name: str):
    """
    Get a currency provider.
    :param db:
    :param name:
    :return:
    """
    return db.query(models.Provider).filter(models.Provider.name == name).first()


def get_currency(db: Session, name: str):
    """
    Get currency.
    :param db:
    :param name:
    :return:
    """
    return db.query(models.Currency).filter(models.Currency.name == name).first()


def create_currency_rate(db: Session, request_date: datetime, currency: int, provider: int,
                         master_currency: int, amount: float):
    """
    Create a new currency rate in the database.
    :param master_currency:
    :param provider:
    :param currency:
    :param request_date:
    :param amount:
    :param db:
    :return: currency_rate
    """
    db_currency_rate = models.CurrencyRate(request_date=request_date, currency=currency, provider=provider,
                                           master_currency=master_currency, amount=amount)
    db.add(db_currency_rate)
    db.commit()
    db.refresh(db_currency_rate)
    return db_currency_rate
