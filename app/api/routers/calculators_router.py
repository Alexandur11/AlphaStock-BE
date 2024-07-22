from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.services.auth_services import get_current_user
from app.api.services.calculators_services import intrinsic_value_calculator, peter_lynch_value_calculator
from app.utilities.service_utilities import stop_if_guest

user_dependency = Annotated[dict, Depends(get_current_user)]

stock_calculator = APIRouter(prefix='/stock_calculator')


@stock_calculator.get('/Intrinsic_value')
async def intrinsic_value(user: user_dependency, symbol: str):
    stop_if_guest(user)
    iv = await intrinsic_value_calculator(symbol)
    return iv


@stock_calculator.get('/peter_lynch_fair_price')
def peter_lynch(user: user_dependency, egr, dy, pe_ratio):
    stop_if_guest(user)
    return peter_lynch_value_calculator(egr, dy, pe_ratio)
