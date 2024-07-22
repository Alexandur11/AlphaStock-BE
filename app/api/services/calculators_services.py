from dotenv import dotenv_values

from app.api.fetches.stock_fetches import fetch_market_data, fetch_cash_flows, fetch_overview
from app.api.services.database_services_inputs import company_overview_db_update
from app.models.alpha_stock import AlphaStock
from alpha_vantage.fundamentaldata import FundamentalData

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)


async def intrinsic_value_calculator(stock):
    market_data = fetch_market_data(stock)
    cash_flows = fetch_cash_flows(stock, Alpha_vintage_key)
    co = fetch_overview(stock.lower())
    income_statement, _ = fd.get_income_statement_annual(stock)
    balance_sheet, _ = fd.get_balance_sheet_annual(stock)

    try:
        AS = AlphaStock(symbol=stock,
                        cash_flows=cash_flows, co=co, market_data=market_data,
                        income_statement=income_statement, balance_sheet=balance_sheet)

        company_overview_db_update(co, stock)
        iv = AS.calculate_intrinsic_value
        return iv

    except Exception as e:
        print(f"Error with {e}")


def peter_lynch_value_calculator(egr, dy, pe_ratio):
    return (float(egr) + float(dy)) / float(pe_ratio)
