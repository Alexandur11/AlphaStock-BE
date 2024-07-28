from app.data.database import read_query


def get_the_list_from_the_db():
    list = read_query('SELECT DISTINCT ticker FROM company')
    return list

