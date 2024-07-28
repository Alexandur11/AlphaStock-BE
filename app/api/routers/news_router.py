from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.fetches.news_fetches import fetch_news_from_alpha_vantage
from app.api.services.auth_services import get_current_user

news_router = APIRouter(prefix='/news')
from app.utilities.service_utilities import stop_if_guest

user_dependency = Annotated[dict, Depends(get_current_user)]


@news_router.get('/')
def stock_news(user:user_dependency,stock:str):
    stop_if_guest(user)
    return fetch_news_from_alpha_vantage(stock)