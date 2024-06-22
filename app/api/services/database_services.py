from app.data.database import insert_query


async def send_parameters_towards_the_database(revenue, net_income, eps, roe, net_profit_margin, debt_level, stock):
    await initiate_years(revenue.keys(), stock)  # turn this only for new stocks
    await revenue_db_update(revenue)
    await net_income_db_update(net_income)
    await eps_db_update(eps)
    await roe_db_update(roe)
    await net_profit_margin_db_update(net_profit_margin,roe)
    await debt_level_db_update(debt_level, stock)

async def initiate_years(years, stock):
    try:
        for x in years:
            await insert_query('INSERT INTO company(ticker, year) values (%s, %s)', (stock, x))
    except Exception as e:
        print(f"Error with initiate_years: {e}")


async def eps_db_update(eps):
    try:
        for x, y in zip(eps.values(), eps.keys()):
            await insert_query('UPDATE company SET eps = %s WHERE year = %s', (float(x), y))
    except Exception as e:
        print(f"Error with eps_db_update: {e}")


async def revenue_db_update(revenue):
    try:
        for x, y in zip(revenue.values(), revenue.keys()):
            await insert_query('UPDATE company SET revenue = %s WHERE year = %s', (x, y))
    except Exception as e:
        print(f"Error with revenue_db_update: {e}")


async def net_income_db_update(net_income):
    try:
        for x, y in zip(net_income.values(), net_income.keys()):
            await insert_query('UPDATE company SET net_income = %s WHERE year = %s', (int(x), y))
    except Exception as e:
        print(f"Error with net_income_db_update: {e}")


async def roe_db_update(roe):
    try:
        for x, y in zip(roe.values(), roe.keys()):
            await insert_query('UPDATE company SET roe = %s WHERE year = %s', (x, y))
    except Exception as e:
        print(f"Error with roe_db_update: {e}")


async def net_profit_margin_db_update(profit_margin, years):
    try:
        for x, y in zip(profit_margin, years.keys()):
            await insert_query('UPDATE company SET profit_margin = %s WHERE year = %s', (x, y))
    except Exception as e:
        print(f"Error with net_profit_margin_db_update: {e}")


async def debt_level_db_update(debt, years):
    try:
        for x, y in zip(debt, years):
            await insert_query('UPDATE company SET debt_level = %s WHERE year = %s', (x, y))
    except Exception as e:
        print(f"Error with debt_level_db_update: {e}")
