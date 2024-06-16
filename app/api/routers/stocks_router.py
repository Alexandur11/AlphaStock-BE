# import requests
# from fastapi import APIRouter
# stocks_router = APIRouter(prefix='/stock')
# from dotenv import dotenv_values
# env_vars = dotenv_values()
#
# Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
#
#
#
#
# @stocks_router.get('/')
# async def fetch_stock_data(symbol):
#     return apple(symbol)
#
#
# def apple(symbol):
#     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={Alpha_vintage_key}'
#     r = requests.get(url)
#     data = r.json()
#
#     return data