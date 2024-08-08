from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.services.auth_services import login_user,register_user,logout_user, get_current_user


user_dependency = Annotated[dict,Depends(get_current_user)]
auth_router = APIRouter(prefix='')


@auth_router.post('/login', status_code=201)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login_user(form_data.username, form_data.password)

@auth_router.post('/register')
async def register(email: str, password: str):
    return await register_user(email, password)

@auth_router.post('/logout')
async def logout(user:user_dependency):
    return await logout_user(user)