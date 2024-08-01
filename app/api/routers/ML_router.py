from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.services.ML_services import ml_stock_prediction
from app.api.services.auth_services import get_current_user
from app.utilities.service_utilities import stop_if_guest
user_dependency = Annotated[dict, Depends(get_current_user)]

ML_router = APIRouter(prefix='/ML_services')


@ML_router.get('/future_price')
def stock_prediction(user: user_dependency, stock: str):
    stop_if_guest(user)
    return ml_stock_prediction(stock)
