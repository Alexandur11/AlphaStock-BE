import bcrypt
import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated
from starlette import status
from jose import jwt, JWTError

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


from app.data.database import read_query
from app.data.database import update_query

from app.utilities.responses import NotFound
from app.utilities.service_utilities import get_user_by_id
from app.utilities.service_utilities import check_existence

load_dotenv()

ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

logged_in_users = {}


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        secret_key = os.getenv('SECRET_KEY')
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("role")

        if email is None or user_id is None:
            raise credentials_exception

        new_token = generate_token({
            'email': email,
            'user_id': user_id,
            'role': user_role,
        })

        user_data = {
            "email": email,
            "id": user_id,
            "role": user_role,
            "new_token": new_token
        }

        return user_data

    except JWTError:
        raise credentials_exception


def generate_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire, 'last_activity': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")})
    secret_key = os.getenv('SECRET_KEY')
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str):
    username_data = read_query('SELECT email FROM users WHERE email = %s', (username,))
    password_data = read_query('SELECT password FROM users WHERE email = %s', (username,))
    if not username_data:
        raise NotFound
    return bcrypt.checkpw(password.encode('utf-8'), password_data[0][0].encode('utf-8'))


def login(username: str, password: str):
    if authenticate_user(username, password) is None:
        raise NotFound

    user_information = read_query('SELECT * FROM users WHERE email = %s', (username,))
    user_token = generate_token({'email': username, 'user_id': user_information[0][0],
                                 'role': user_information[0][3]})

    logged_in_users.update({f'{user_information[0][0]}': {'Email': username}})
    return {
        "access_token": user_token,
        "token_type": "bearer"
    }


def logout(user_id: int):
    user = get_user_by_id(user_id)
    if user and str(user_id) in logged_in_users:
        logged_in_users.popitem()
        return {'message': 'You have successfully logged out!'}
    else:
        raise NotFound


async def register(email: str, password: str):
    check_existence(email)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    update_query('INSERT INTO users(email,password) VALUES(%s, %s)', (email, hashed_password))

    return {"message": "User registered successfully!"}
