from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.orm import relationship

from .database import Base


# owner = relationship("User", back_populates="items")

class Currency(Base):
    __tablename__ = "Currency"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)


class Provider(Base):
    __tablename__ = "Provider"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)


class CurrencyRate(Base):
    __tablename__ = "CurrencyRate"

    id = Column(Integer, primary_key=True)
    request_date = Column(Date, nullable=False, index=True)
    currency = relationship("Currency")
    provider = relationship("Provider")
    master_currency = relationship("Currency")
    amount = Column(Numeric, default=0)
