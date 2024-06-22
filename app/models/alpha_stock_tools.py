import pandas as pd

class AlphaStockTools():
    @staticmethod
    def calculate_revenue_growth(revenues):
        try:
            growth_rates = []
            for i in range(1, len(revenues)):
                growth_rate = (revenues[i] - revenues[i - 1]) / revenues[i - 1]
                growth_rates.append(growth_rate)
            return growth_rates
        except Exception as e:
            print(f"Error calculating revenue at calculate_revenue_growth: {e}")
            return None

    @staticmethod
    def calculate_ROE(net_incomes, total_assets, total_liabilities, years):
        try:
            incomes = [int(x) for x in net_incomes.values()]
            shareholders_equity = [int(asset) - int(liability) for asset, liability in
                                   zip(total_assets, total_liabilities)]  # Formula for SQ

            ROE_14_Y = [net_income - sq for net_income, sq in zip(incomes, shareholders_equity)]  # Formula for ROE

            result = {d: v for d, v in zip(years, ROE_14_Y)}

            return result
        except Exception as e:
            print(f"Error calculating roe: {e}")
            return None

    @staticmethod
    def calculate_net_profit_margin(total_revenues, net_income):
        try:
            all_incomes = [int(x) for x in net_income.values()]
            results = [int(n) // int(r) * 100 for n, r in zip(all_incomes, total_revenues)]

            return results
        except Exception as e:
            print(f"Error calculating net profit margin: {e}")
            return None


