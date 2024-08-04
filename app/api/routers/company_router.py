from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.fetches.stock_fetches import fetch_overview
from app.api.services.auth_services import get_current_user
from app.api.services.company_services import financial_performance, company_info_from_db
from app.utilities.service_utilities import stop_if_guest
from fastapi.responses import StreamingResponse

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
    co = fetch_overview(symbol.lower())
    return co


@company_router.get('/information')
def company_information(user: user_dependency, symbol: str):
    stop_if_guest(user)
    ci = company_info_from_db(symbol.lower())
    return StreamingResponse(ci, media_type="image/png")
