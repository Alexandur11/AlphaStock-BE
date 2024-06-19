from app.data.database import insert_query


def send_parameters_towards_the_database(revenue,net_income,eps,roe,net_profit_margin, stock):
    initiate_years(revenue.keys(), stock) # turn this only only for new stocks
    revenue_db_update(revenue.values(),revenue.keys())
    net_income_db_update(net_income.values(), net_income.keys())
    eps_db_update(eps.values(), eps.keys())
    roe_db_update(roe.values(), roe.keys())
    net_profit_margin_db_update(net_profit_margin, roe.keys())



def initiate_years(years, stock):
    for x in years:
        insert_query('INSERT INTO company(year, ticker) values (%s, %s)', (x, stock))


def eps_db_update(eps, years):
    for x, y in zip(eps, years):
        insert_query('UPDATE company SET eps = %s WHERE year = %s', (float(x),y))

def revenue_db_update(revenue, years):
    for x, y in zip(revenue, years):
        insert_query('UPDATE company SET revenue = %s WHERE year = %s', (x,y))

def net_income_db_update(net_income, years):
    for x, y in zip(net_income, years):
        insert_query('UPDATE company SET net_income = %s WHERE year = %s', (int(x),y))


def roe_db_update(roe, years):
    for x, y in zip(roe, years):
        insert_query('UPDATE company SET roe = %s WHERE year = %s', (x,y))

def net_profit_margin_db_update(profit_margin, years):
    for x, y in zip(profit_margin, years):
        insert_query('UPDATE company SET profit_margin = %s WHERE year = %s', (x,y))




