from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values

from app.api.services.database_services import send_parameters_towards_the_database
from app.api.fetches.stock_fetches import fetch_annual_eps
from app.models.alpha_stock import AlphaStock

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)


async def financial_performance(stock):
    income_statement, _ = fd.get_income_statement_annual(stock)  # fetch  income statement
    balance_sheet, _ = fd.get_balance_sheet_annual(stock)  # fetch balance sheet
    annual_eps = fetch_annual_eps(stock, Alpha_vintage_key)  # fetch annual eps

    AS = AlphaStock(stock, income_statement, balance_sheet, annual_eps)

    revenue_for_14_years = AS.revenue
    net_income_for_14_years = AS.net_income
    eps_for_14_years = AS.eps
    roe_for_14_years = AS.roe
    net_profit_margin_for_14_years = AS.net_profit_margin
    debt_level_for_14_years = AS.debt

    await send_parameters_towards_the_database(revenue_for_14_years,
                                               net_income_for_14_years,
                                               eps_for_14_years,
                                               roe_for_14_years,
                                               net_profit_margin_for_14_years,
                                               debt_level_for_14_years,
                                               stock)
    return 'Parameters successfully fetched and registered'
