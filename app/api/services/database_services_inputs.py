from app.data.database import insert_query, read_query
from datetime import datetime


async def send_parameters_towards_the_database(revenue, net_income, eps, roe,
                                               net_profit_margin, debt_level, cash_flows, stock):
    check_for_existence = read_query('SELECT year, ticker FROM company WHERE symbol = %s', (stock,))
    if len(check_for_existence) >= 13:
        return
    else:
        initiate_years(revenue, stock)  # turn this only for new stocks
        revenue_db_update(revenue, stock)
        net_income_db_update(net_income, stock)
        eps_db_update(eps, stock)
        roe_db_update(roe, stock)
        net_profit_margin_db_update(net_profit_margin, stock)
        debt_level_db_update(debt_level, stock)
        cash_flows_db_update(cash_flows, stock)


def initiate_years(years, stock):
    try:
        for x in years['fiscalDateEnding']:
            insert_query('INSERT INTO company(ticker, year) values (%s, %s)', (stock, x))
    except Exception as e:
        print(f"Error with initiate_years: {e}")


def eps_db_update(eps, stock):
    try:
        for x, y in zip(eps['reportedEPS'], eps['fiscalDateEnding']):
            insert_query('UPDATE company SET eps = %s WHERE year = %s AND ticker = %s', (float(x), y, stock))
    except Exception as e:
        print(f"Error with eps_db_update: {e}")


def revenue_db_update(revenue, stock):
    try:
        for x, y in zip(revenue['growth_rate'], revenue['fiscalDateEnding']):
                insert_query('UPDATE company SET revenue = %s WHERE year = %s AND ticker = %s', (x, y, stock))
    except Exception as e:
        print(f"Error with revenue_db_update: {e}")


def net_income_db_update(net_income, stock):
    try:
        for x, y in zip(net_income['netIncome'], net_income['fiscalDateEnding']):
            insert_query('UPDATE company SET net_income = %s WHERE year = %s AND ticker = %s', (int(x), y, stock))
    except Exception as e:
        print(f"Error with net_income_db_update: {e}")


def roe_db_update(roe, stock):
    try:
        for x, y in zip(roe['roe'], roe['fiscalDateEnding']):
            insert_query('UPDATE company SET roe = %s WHERE year = %s AND ticker = %s', (x, y, stock))
    except Exception as e:
        print(f"Error with roe_db_update: {e}")


def net_profit_margin_db_update(profit_margin, stock):
    try:
        for x, y in zip(profit_margin['netProfitMargin'], profit_margin['fiscalDateEnding']):
            insert_query('UPDATE company SET profit_margin = %s WHERE year = %s AND ticker = %s', (x, y, stock))
    except Exception as e:
        print(f"Error with net_profit_margin_db_update: {e}")


def debt_level_db_update(debt, stock):
    try:
        for x, y in zip(debt['currentDebt'], debt['fiscalDateEnding']):
            insert_query('UPDATE company SET debt_level = %s WHERE year = %s AND ticker = %s', (x, y, stock))
    except Exception as e:
        print(f"Error with debt_level_db_update: {e}")


def cash_flows_db_update(cash_flows, stock):
    try:
        for x, y in zip(cash_flows['operatingCashflow'], cash_flows['fiscalDateEnding']):
           insert_query('UPDATE company SET cash_flow = %s WHERE year = %s AND ticker = %s', (x, y, stock))
    except Exception as e:
        print(f"Error with debt_level_db_update: {e}")

def company_overview_db_update(company_overview, stock):
    # Q1: October 1 - December 31
    # Q2: January 1 - March 31
    # Q3: April 1 - June 30
    # Q4: July 1 - September 30

    check_existence = read_query('SELECT symbol FROM company_overview WHERE symbol = %s AND quarter = %s',
                                 (stock, company_overview['LatestQuarter']))

    if not check_existence:
        insert_query("""INSERT INTO company_overview (
                        Symbol, asset_type, quarter, market_capitalization, ebitda, 
                        pe_ratio, peg_ratio, book_value, dividend_per_share, dividend_yield, 
                        eps, revenue_per_share, profit_margin, operating_margin, 
                        return_on_asset, return_on_equity, revenue, gross_profit, 
                        diluted_eps, quarterly_earnings_growth, quarterly_revenue_growth, 
                        analyst_target_price, analyst_rating_strong_buy, analyst_rating_buy, 
                        analyst_rating_hold, analyst_rating_sell, analyst_rating_strong_sell, 
                        trailing_pe, forward_pe, price_to_sales_ratio, price_to_book_ratio, 
                        ev_to_revenue, ev_to_ebitda, beta, Year52WeekHigh, Year52WeekLow, 
                        MovingAverage50Day, MovingAverage200Day, shares_outstanding
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s
                    )""",

                     (company_overview['Symbol'], company_overview['AssetType'],
                      company_overview['LatestQuarter'], company_overview['MarketCapitalization'],
                      company_overview['EBITDA'], company_overview['PERatio'],
                      company_overview['PEGRatio'], company_overview['BookValue'],
                      company_overview['DividendPerShare'], company_overview['DividendYield'],
                      company_overview['EPS'], company_overview['RevenuePerShareTTM'],
                      company_overview['ProfitMargin'], company_overview['OperatingMarginTTM'],
                      company_overview['ReturnOnAssetsTTM'], company_overview['ReturnOnEquityTTM'],
                      company_overview['RevenueTTM'], company_overview['GrossProfitTTM'],
                      company_overview['DilutedEPSTTM'], company_overview['QuarterlyEarningsGrowthYOY'],
                      company_overview['QuarterlyRevenueGrowthYOY'], company_overview['AnalystTargetPrice'],
                      company_overview['AnalystRatingStrongBuy'],company_overview['AnalystRatingBuy'],
                      company_overview['AnalystRatingHold'], company_overview['AnalystRatingSell'],
                      company_overview['AnalystRatingStrongSell'], company_overview['TrailingPE'],
                      company_overview['ForwardPE'], company_overview['PriceToSalesRatioTTM'],
                      company_overview['PriceToBookRatio'], company_overview['EVToRevenue'],
                      company_overview['EVToEBITDA'], company_overview['Beta'], company_overview['52WeekHigh'],
                      company_overview['52WeekLow'], company_overview['50DayMovingAverage'], company_overview['200DayMovingAverage'],
                      company_overview['SharesOutstanding']))

    return "success"
