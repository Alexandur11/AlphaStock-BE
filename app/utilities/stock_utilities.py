import pandas as pd


def calculate_revenue_growth(revenues):
    growth_rates = []
    for i in range(1, len(revenues)):
        growth_rate = (revenues[i] - revenues[i - 1]) / revenues[i - 1]
        growth_rates.append(growth_rate)
    return growth_rates

def calculate_ROE(net_incomes, balance_sheet):
    # net_df = pd.DataFrame(net_incomes)
    bal_df = pd.DataFrame(balance_sheet)
    incomes = [int(x) for x in net_incomes]

    total_assets = bal_df['totalAssets'].tolist()
    total_liabilities = bal_df['totalLiabilities'].tolist()

    shareholders_equity = [int(asset) - int(liability) for asset,liability in zip(total_assets, total_liabilities)] # Formula for SQ


    ROE_14_Y = [net_income - sq for net_income, sq in zip(incomes, shareholders_equity)] # Formula for ROE

    years = balance_sheet.get('fiscalDateEnding')
    result = {d:v for d,v in zip(years, ROE_14_Y)}

    return result



def calculate_net_profit_margin(income_statement, net_income):

    df = pd.DataFrame(income_statement)

    # Extract revenues and parse dates
    revenues = df['totalRevenue'].astype(int).tolist()
    all_incomes = [int(x) for x in net_income]



    results = [int(n)//int(r) * 100 for n,r in zip(all_incomes, revenues)]

    return results


def calculate_debt_level(balance_sheet, stock):
    debt = balance_sheet.get('currentDebt')
    years = balance_sheet.get('fiscalDateEnding')

    data = {year: debt for year, debt in zip(years, debt)}

    return data

