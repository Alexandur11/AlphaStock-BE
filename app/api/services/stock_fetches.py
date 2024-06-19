import requests
from dotenv import dotenv_values

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')

def fetch_annual_eps(stock, Alpha_vintage_key):
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data.get('annualEarnings', [])

def stock_minutes(stock: str, min: int):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval={min}min&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data

def stock_days(stock: str):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def stock_weeks(stock: str):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def stock_months(stock: str):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def stock_latest(stock: str):

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data