from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import dotenv_values

from app.api.services.core_stock_services import revenue, eps, net_income
from app.api.services.database_services import send_parameters_towards_the_database
from app.api.services.stock_fetches import fetch_annual_eps
from app.utilities.stock_utilities import  calculate_ROE, calculate_net_profit_margin

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)




def financial_performance(stock):
    income_statement, _ = fd.get_income_statement_annual(stock) # fetch  income statement
    balance_sheet, _ = fd.get_balance_sheet_annual(stock) # fetch balance sheet


    revenue_for_14_years = revenue(income_statement) # Calculate the revenue, year per year for 14 years
    net_income_for_14_years = net_income(income_statement) # Pick Net incomes from income statement

    eps_for_14_years = eps(stock) # fetch annual eps
    roe_for_14_years = calculate_ROE(list(net_income_for_14_years.values()), balance_sheet) # Calculate roe for 14 years

    net_profit_margin_for_14_years = calculate_net_profit_margin(
        income_statement, list(net_income_for_14_years.values())) # Calculate NPM for 14 years


    send_parameters_towards_the_database(revenue_for_14_years, net_income_for_14_years,
                                         eps_for_14_years, roe_for_14_years,net_profit_margin_for_14_years, stock)
