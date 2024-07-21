from typing import Annotated
import json
from urllib.request import urlopen

from fastapi import APIRouter, Depends

from app.api.fetches.stock_fetches import fetch_overview, fetch_data_with_safari
from app.api.services.auth_services import get_current_user
from app.api.services.company_services import financial_performance, intrinsic_value_calculator, \
    peter_lynch_value_calculator, company_info_from_db

from app.utilities.service_utilities import stop_if_guest

user_dependency = Annotated[dict, Depends(get_current_user)]

company_router = APIRouter(prefix='/company')


@company_router.get('/Financial_performance')
async def company_financial_performance(user: user_dependency, symbol: str):
    stop_if_guest(user)
    fp = await financial_performance(symbol.lower())
    return fp


@company_router.get('/Company_overview')
async def company_overview(user: user_dependency, symbol: str):
    stop_if_guest(user)
    co = await fetch_overview(symbol.lower())
    return co

@company_router.get('/Intrinsic_value')
async def intrinsic_value(user:user_dependency, symbol:str):
    stop_if_guest(user)
    iv = await intrinsic_value_calculator(symbol)
    return iv

@company_router.get('/peter_lynch_fair_price')
def peter_lynch(egr,dy,pe_ratio):
    return peter_lynch_value_calculator(egr,dy,pe_ratio)

@company_router.get('/information')
def company_information(stock:str):
    ci = company_info_from_db(stock.lower())
    return ci
