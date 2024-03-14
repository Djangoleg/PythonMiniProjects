from pydantic import BaseModel


class CurrencyRateRequest(BaseModel):
    """
    Request schema.
    """
    currencies_source: list[str] = None
    currency_target: str = None
