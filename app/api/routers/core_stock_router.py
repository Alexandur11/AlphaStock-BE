from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.fetches.stock_fetches import stock_minutes, stock_days, stock_weeks, \
    stock_months, stock_latest
from app.api.services.auth_services import get_current_user
from app.utilities.service_utilities import stop_if_guest

user_dependency = Annotated[dict, Depends(get_current_user)]
stocks_router = APIRouter(prefix='/stock')




@stocks_router.get('/minutes')
async def stock_per_minute(user: user_dependency, symbol: str, min: int):
    stop_if_guest(user)
    return stock_minutes(symbol, min)

@stocks_router.get('/day')
async def stock_per_day(user: user_dependency, symbol: str):
    stop_if_guest(user)
    return stock_days(symbol)

@stocks_router.get('/week')
async def stock_per_week(user: user_dependency, symbol: str):
    stop_if_guest(user)

    return stock_weeks(symbol)

@stocks_router.get('/week')
async def stock_per_month(user:user_dependency, symbol: str):
    stop_if_guest(user)
    return stock_months(symbol)

@stocks_router.get('/week')
async def stock_latest_price(user:user_dependency,symbol: str):
    stop_if_guest(user)
    return stock_latest(symbol)

# @stocks_router.get('/revenue')
# async def stock_revenue(user:user_dependency, symbol:str):
#     stop_if_guest(user)
#     return revenue(symbol)
#
# @stocks_router.get('/debt')
# def company_debt(user: user_dependency, symbol: str):
#     stop_if_guest(user)
#     return debt(symbol)
#
# @stocks_router.get('ROE')
# def company_roe(user:user_dependency, symbol:str):
#     stop_if_guest(user)
#     return roe(symbol)
#
# @stocks_router.get('EPS')
# def company_eps(user:user_dependency, symbol:str):
#     stop_if_guest(user)
#     return eps(symbol)
#
