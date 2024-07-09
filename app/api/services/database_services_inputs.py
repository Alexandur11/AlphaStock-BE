from app.data.database import insert_query


async def send_parameters_towards_the_database(revenue, net_income, eps, roe,
                                               net_profit_margin, debt_level, cash_flows, stock):
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
