# import pandas as pd
#
#
# def calculate_revenue_growth(revenues):
#     try:
#         growth_rates = []
#         for i in range(1, len(revenues)):
#             growth_rate = (revenues[i] - revenues[i - 1]) / revenues[i - 1]
#             growth_rates.append(growth_rate)
#         return growth_rates
#     except Exception as e:
#         print(f"Error calculating revenue at calculate_revenue_growth: {e}")
#         return None
#
#
# def calculate_ROE(net_incomes, balance_sheet):
#     try:
#         bal_df = pd.DataFrame(balance_sheet)
#         incomes = [int(x) for x in net_incomes]
#
#         total_assets = bal_df['totalAssets'].tolist()
#         total_liabilities = bal_df['totalLiabilities'].tolist()
#
#         shareholders_equity = [int(asset) - int(liability) for asset,liability in zip(total_assets, total_liabilities)] # Formula for SQ
#
#
#         ROE_14_Y = [net_income - sq for net_income, sq in zip(incomes, shareholders_equity)] # Formula for ROE
#
#         years = balance_sheet.get('fiscalDateEnding')
#         result = {d:v for d,v in zip(years, ROE_14_Y)}
#
#         return result
#     except Exception as e:
#         print(f"Error calculating roe: {e}")
#         return None
#
#
# def calculate_net_profit_margin(income_statement, net_income):
#     try:
#         df = pd.DataFrame(income_statement)
#         revenues = df['totalRevenue'].astype(int).tolist()
#         all_incomes = [int(x) for x in net_income]
#         results = [int(n)//int(r) * 100 for n,r in zip(all_incomes, revenues)]
#
#         return results
#     except Exception as e:
#         print(f"Error calculating net profit margin: {e}")
#         return None
#
#
from app.api.fetches.stock_fetches import fetch_overview
from app.data.database import read_query


def quarterly_overview(overview):
    info = read_query('SELECT * from company_overview WHERE Symbol = %s AND LatestQuarter = %s',
               (overview['Symbol'], overview['LatestQuarter']))
    if info:
        return info
    else:
        pass
        # co = await fetch_overview(symbol.lower())
