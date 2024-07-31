from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.services.auth_services import login, logout, register
from app.api.services.auth_services import get_current_user
user_dependency = Annotated[dict, Depends(get_current_user)]

login_router = APIRouter(prefix='/login')
logout_router = APIRouter(prefix='/logout')
register_router = APIRouter(prefix='/register')

all_users = {}


@login_router.post('', status_code=201)
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    This method takes the user's email and password, logs them in, and returns a token.
    """
    return login(form_data.username, form_data.password)


@register_router.post('')
async def register_user(email: str, password: str):
    return await register(email, password)
