from typing import Annotated

from fastapi import APIRouter, Depends
from dotenv import dotenv_values

from app.api.services.core_stock_services import stock_minutes, stock_days, stock_weeks, \
    stock_months, stock_latest, revenue, debt
from app.api.services.login_services import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
stocks_router = APIRouter(prefix='/stock')




@stocks_router.get('/minutes')
async def stock_per_minute(user: user_dependency, symbol: str, min: int):
    return stock_minutes(user, symbol, min)

@stocks_router.get('/day')
async def stock_per_day(user: user_dependency, symbol: str):
     return stock_days(user, symbol)

@stocks_router.get('/week')
async def stock_per_week(user: user_dependency, symbol: str):
    return stock_weeks(user, symbol)

@stocks_router.get('/week')
async def stock_per_month(user:user_dependency, symbol: str):
    return stock_months(user, symbol)

@stocks_router.get('/week')
async def stock_latest_price(user:user_dependency,symbol: str):
    return stock_latest(user, symbol)

@stocks_router.get('/revenue')
async def stock_revenue(user:user_dependency, symbol:str):
    return revenue(user, symbol)

@stocks_router.get('/debt')
def company_debt(user: user_dependency, symbol: str):
    return debt(user, symbol)
