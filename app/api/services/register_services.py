import bcrypt

from app.data.database import update_query
from app.utilities.service_utilities import check_existence

async def register(email:str, password:str):
    check_existence(email)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    update_query('INSERT INTO users(email,password) VALUES(%s, %s)', (email, hashed_password))

    return {"message": "User registered successfully!"}
