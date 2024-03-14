from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal
from .schemas import CurrencyRateRequest

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/currency/rate/")
async def get_currency_rate(request: CurrencyRateRequest, db: Session = Depends(get_db)):
    if request is None:
        raise HTTPException(status_code=404, detail="Request data is empty")

    if request.currency_target is None or not request.currency_target:
        raise HTTPException(status_code=404, detail="Field currency_target is empty")

    if request.currencies_source is None or len(request.currencies_source) == 0:
        raise HTTPException(status_code=404, detail="Field currencies_source is empty")

    return {"message": "Hello, Currency"}
