from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.services.company_services import financial_performance
from app.api.services.login_services import get_current_user
from app.utilities.service_utilities import stop_if_guest

user_dependency = Annotated[dict, Depends(get_current_user)]

company_router = APIRouter(prefix='/company')

@company_router.get('/Financial_performance')
async def company_financial_performance(user:user_dependency, symbol:str):
    stop_if_guest(user)
    fp = await financial_performance(symbol)
    return "14 years of information collected, parsed and sent towards the database"