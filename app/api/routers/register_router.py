from fastapi import APIRouter

from app.api.services.register_services import register

register_router = APIRouter(prefix='/register')

@register_router.post('')
async def register_user(email: str, password: str):
    return await register(email, password)
