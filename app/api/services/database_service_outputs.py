from app.data.database import read_query


def fetch_eps_from_database(symbol):
        eps =  read_query('SELECT eps FROM company WHERE ticker = %s ORDER BY year ASC', (symbol,))
        years = read_query('SELECT year FROM company WHERE ticker = %s', (symbol,))
        return eps,years
