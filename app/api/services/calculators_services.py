from dotenv import dotenv_values

from app.api.fetches.stock_fetches import fetch_market_data, fetch_cash_flows, fetch_overview
from app.api.services.database_services_inputs import company_overview_db_update
from app.models.alpha_stock import AlphaStock
from alpha_vantage.fundamentaldata import FundamentalData

env_vars = dotenv_values()
Alpha_vintage_key = env_vars.get('ALPHA_VANTAGE_KEY')
fd = FundamentalData(Alpha_vintage_key)


async def intrinsic_value_calculator(symbol):
    market_data = fetch_market_data(symbol)
    cash_flows = fetch_cash_flows(symbol, Alpha_vintage_key)
    co = fetch_overview(symbol.lower())
    income_statement, _ = fd.get_income_statement_annual(symbol)
    balance_sheet, _ = fd.get_balance_sheet_annual(symbol)

    try:
        AS = AlphaStock(symbol=symbol,
                        cash_flows=cash_flows, co=co, market_data=market_data,
                        income_statement=income_statement, balance_sheet=balance_sheet)

        company_overview_db_update(co, symbol)
        iv = AS.calculate_intrinsic_value_per_share
        return iv

    except Exception as e:
        return (f"Error with {e}")


def peter_lynch_value_calculator(egr, dy, pe_ratio):
    try:
        return (float(egr) + float(dy)) / float(pe_ratio)
    except Exception as e:
        return (f"There was a problem with the injected parameters {e}")

