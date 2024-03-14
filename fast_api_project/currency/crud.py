from sqlalchemy.orm import Session

from currency import models
from currency.schemas import CurrencyRateCreate


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


def create_currency_rate(db: Session, cr: CurrencyRateCreate):
    """
    Create a new currency rate in the database.
    :param db:
    :param cr:
    :return: currency_rate
    """
    db_currency_rate = models.CurrencyRate(request_date=cr.request_date, currency=cr.currency, provider=cr.provider,
                                           master_currency=cr.master_currency, amount=cr.amount)
    db.add(db_currency_rate)
    db.commit()
    db.refresh(db_currency_rate)
    return db_currency_rate
