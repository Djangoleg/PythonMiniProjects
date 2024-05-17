from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, event, DateTime
from sqlalchemy.orm import relationship

from .database import Base, engine


# Define a User model for your database
class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Currency(Base):
    __tablename__ = "Currency"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    def __str__(self):
        return self.name


class Provider(Base):
    __tablename__ = "Provider"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    def __str__(self):
        return self.name


class CurrencyRate(Base):
    __tablename__ = "CurrencyRate"

    id = Column(Integer, primary_key=True)
    request_date = Column(DateTime(timezone=True), index=True, default=datetime.now(timezone.utc))
    currency_id = Column(Integer, ForeignKey('Currency.id'), index=True)
    currency = relationship("Currency", primaryjoin="Currency.id == CurrencyRate.currency_id")
    provider_id = Column(Integer, ForeignKey('Provider.id'), index=True)
    provider = relationship("Provider", primaryjoin="Provider.id == CurrencyRate.provider_id")
    master_currency_id = Column(Integer, ForeignKey('Currency.id'), index=True)
    master_currency = relationship("Currency", primaryjoin="Currency.id == CurrencyRate.master_currency_id")
    amount = Column(Numeric, default=0)


@event.listens_for(Provider.__table__, 'after_create')
def insert_provider(target, connection, **kwargs):
    """
    Fill Provider after create.
    :param target:
    :param connection:
    :param kwargs:
    :return:
    """
    currency_provider = ["CBRF", "Currencylayer"]

    for ind, prov in enumerate(currency_provider, start=1):
        connection.execute(target.insert(), {'id': ind, 'name': prov})


@event.listens_for(Currency.__table__, 'after_create')
def insert_currency(target, connection, **kwargs):
    """
    Fill Currency after create.
    :param target:
    :param connection:
    :param kwargs:
    :return:
    """
    currencies_source = ["USD", "EUR", "GBP", "UAH", "CNY", "RUB"]

    for ind, curr in enumerate(currencies_source, start=1):
        connection.execute(target.insert(), {'id': ind, 'name': curr})


@event.listens_for(User.__table__, 'after_create')
def insert_user(target, connection, **kwargs):
    hashed_password = '1adf87ecdc7eb0c5b27760c96df35ea50026a39804c453fe4ccc07474a550597'
    connection.execute(target.insert(), {'id': 1, 'username': 'post', 'password': hashed_password})


# Create database and table.
Base.metadata.create_all(engine)
