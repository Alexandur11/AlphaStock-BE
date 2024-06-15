from pydantic import Field
from app.data.database import read_query
from app.utilities.responses import EmailExists


def get_user_by_id(user_id: int = Field(gt=0)):
    result = read_query("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return result


def check_existence(email):
    info = read_query('SELECT * FROM users WHERE email = %s',(email,))
    if info:
        raise EmailExists