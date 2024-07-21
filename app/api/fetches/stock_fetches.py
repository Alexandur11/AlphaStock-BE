import pandas as pd
import requests
from dotenv import dotenv_values
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')

def fetch_annual_eps(stock, Alpha_vintage_key):
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data.get('annualEarnings', [])

def fetch_cash_flows(stock, Alpha_vintage_key):
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data


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

def stock_monthly_adjusted(stock:str):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def stock_latest(stock: str):

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()

    return data


def fetch_overview(stock):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock}&apikey={Alpha_vintage_key}'
    r = requests.get(url)
    data = r.json()
    return data

def fetch_beta(stock):

    #Yahoo
    stock_data = yf.Ticker(stock)
    historical_data = stock_data.history(period="max")

    # Calculate beta
    beta = historical_data['Close'].pct_change().cov(historical_data['Close'].pct_change())

    return beta

def fetch_market_data(stock):

    # Yahoo
    market_data = yf.download(f'{stock}', start='2010-01-01', end='2023-01-01')
    return market_data



def fetch_data_with_safari(stock):
    url = f'https://finance.yahoo.com/quote/{stock}/analysis/'
    # Initialize SafariDriver
    driver = webdriver.Safari()

    # Open the URL
    driver.get(url)

    try:
        # Wait until the consent pop-up is present
        consent_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'cookie-consent'))
        )

        # Click the accept button
        accept_button = consent_div.find_element(By.ID, 'decline-cookies')
        accept_button.click()
    except Exception as e:
        print(f"No cookie consent pop-up found: {e}")

    # Extract data or interact with the page
    # Example: Print page title
    print(driver)