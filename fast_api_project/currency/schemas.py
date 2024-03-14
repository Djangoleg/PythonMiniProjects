from datetime import datetime

from pydantic import BaseModel


class CurrencyRateRequestData(BaseModel):
    """
    Request schema.
    """
    currencies_source: list[str] = None
    currency_target: str = None

    def __str__(self):
        return (f"Incoming request:\n{{\n\tcurrencies_source: "
                f"{self.currencies_source},\n\tcurrency_target: {self.currency_target}\n}}")


class CurrencyRateCreate(BaseModel):
    """
    Currency rate create schema.
    """
    request_date: datetime = datetime.now()
    currency: int
    provider: int
    master_currency: int
    amount: float
