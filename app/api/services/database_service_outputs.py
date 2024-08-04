from app.data.database import read_query


def fetch_eps_from_database(symbol):
    try:
        eps = read_query('SELECT eps FROM company WHERE symbol = %s ORDER BY year ASC', (symbol,))
        years = read_query('SELECT year FROM company WHERE symbol = %s', (symbol,))
        return eps, years
    except Exception as e:
        return f"Error with fetching from the database "
