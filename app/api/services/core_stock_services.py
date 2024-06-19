import requests
from dotenv import dotenv_values
import json

from app.api.services.stock_fetches import fetch_annual_eps
from app.utilities.stock_utilities import calculate_revenue_growth, calculate_debt_level
from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd


env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)



def revenue(income_statement):
    try:

        # Convert to DataFrame
        df = pd.DataFrame(income_statement)

        # Extract revenues and parse dates
        revenues = df['totalRevenue'].astype(int).tolist()
        dates = pd.to_datetime(df['fiscalDateEnding'])

        # Calculate revenue growth
        revenue_growth = calculate_revenue_growth(revenues)

        # Create a list of formatted years and growth rates
        years = [str(date) for date in dates]  # Reverse order of dates and convert to string
        growth_rates = [f"{growth * 100:.2f}%" for growth in
                        revenue_growth]  # Reverse order of growth rates and format

        # Create a dictionary in the desired JSON structure
        data = {year: growth for year, growth in zip(years, growth_rates)}

        return data

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return None


def debt(stock: str, balance_sheet):
    try:
        debt = calculate_debt_level(balance_sheet, stock)
        return debt

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return None



def eps(stock: str):
    earnings = fetch_annual_eps(stock, Alpha_vintage_key)
    try:
        df = pd.DataFrame(earnings)
        dates = pd.to_datetime(df['fiscalDateEnding'])
        eps_ratings = df['reportedEPS'].tolist()

        years = [str(date) for date in dates]
        data = {years: eps_rating for years, eps_rating in zip(years, eps_ratings)}

        return  data
    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return None

def net_income(income_statement):
    try:
        df = pd.DataFrame(income_statement)
        dates = pd.to_datetime(df['fiscalDateEnding'])
        net  = df['netIncome'].tolist()
        years = [str(date) for date in dates]


        data = {years:net for years, net in zip(years, net)}

        return data
    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return None