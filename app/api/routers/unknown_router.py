from app.api.services.unknown_services import get_the_list_from_the_db
from fastapi import  APIRouter

unknown_router = APIRouter(prefix='/unknown')

@unknown_router.get('/')
async def list_of_stocks():
    list = get_the_list_from_the_db()
    return list
