import requests
from dotenv import dotenv_values
from app.utilities.stock_utilities import calculate_revenue_growth
from app.utilities.service_utilities import stop_if_guest
from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd
import numpy as np





env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)


Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')

def stock_minutes(user, stock: str, min: int):
    stop_if_guest(user)

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval={min}min&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data

def stock_days(user, stock: str):
    stop_if_guest(user)

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data

def stock_weeks(user, stock:str):
    stop_if_guest(user)

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data

def stock_months(user, stock:str):
    stop_if_guest(user)

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data

def stock_latest(user, stock:str):
    stop_if_guest(user)

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data

def revenue(user, stock: str):
    stop_if_guest(user)

    try:
        # Fetch the income statement from Alpha Vantage
        income_statement, _ = fd.get_income_statement_annual(stock)

        # Convert to DataFrame
        df = pd.DataFrame(income_statement)

        # Extract revenues and parse dates
        revenues = df['totalRevenue'].astype(int).tolist()
        dates = pd.to_datetime(df['fiscalDateEnding'])


        # Calculate revenue growth
        revenue_growth = calculate_revenue_growth(revenues)

        # Create a list of formatted years and growth rates
        years = [str(date) for date in dates[::-1]]  # Reverse order of dates and convert to string
        growth_rates = [f"{growth * 100:.2f}%" for growth in
                        revenue_growth[::-1]]  # Reverse order of growth rates and format

        # Create a dictionary in the desired JSON structure
        data = {year:growth for year, growth in zip(years,growth_rates)}

        return {"The Revenue growth year-over-year for": stock}, data

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return None



def debt(user, stock:str):
    stop_if_guest(user)  # Assuming this is a function that checks if the user is a guest

    try:
        # Fetch balance sheet data from Alpha Vantage
        balance_sheet, _ = fd.get_balance_sheet_annual(stock)


        debt = balance_sheet.get('currentDebt')[::-1]
        years = balance_sheet.get('fiscalDateEnding')[::-1]

        data = {year:debt for year, debt in zip(years,debt)}

        return {"The debt for year-over-year for": stock}, data

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return None