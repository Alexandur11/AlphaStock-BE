import pandas as pd

from app.models.alpha_stock_tools import AlphaStockTools as AST


class AlphaStock(AST):
    def __init__(self, symbol: str, income_statement, balance_sheet, annual_eps):
        self.symbol = symbol
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.annual_eps = annual_eps

    @property
    def revenue(self):
        try:

            # Convert to DataFrame
            df = pd.DataFrame(self.income_statement)

            # Extract revenues and parse dates
            revenues = df['totalRevenue'].astype(int).tolist()
            dates = pd.to_datetime(df['fiscalDateEnding'])

            # Calculate revenue growth
            revenue_growth = AST.calculate_revenue_growth(revenues)

            # Create a list of formatted years and growth rates
            years = [str(date) for date in dates]
            growth_rates = [f"{growth * 100:.2f}%" for growth in
                            revenue_growth]

            # Create a dictionary in the desired JSON structure
            data = {year: growth for year, growth in zip(years, growth_rates)}

            return data

        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def debt(self):
        try:
            debt = self.balance_sheet.get('currentDebt').tolist()
            return debt
        except Exception as e:
            print(f"Error calculating debt level: {e}")
            return None

    @property
    def net_income(self):
        try:
            df = pd.DataFrame(self.income_statement)
            dates = pd.to_datetime(df['fiscalDateEnding'])
            net = df['netIncome'].tolist()
            years = [str(date) for date in dates]

            data = {years: net for years, net in zip(years, net)}

            return data
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def eps(self):
        try:
            df = pd.DataFrame(self.annual_eps)
            dates = pd.to_datetime(df['fiscalDateEnding'])
            eps_ratings = df['reportedEPS'].tolist()

            years = [str(date) for date in dates]
            data = {years: eps_rating for years, eps_rating in zip(years, eps_ratings)}

            return data
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def net_profit_margin(self):
        try:
            df = pd.DataFrame(self.income_statement)
            total_revenues = df['totalRevenue'].astype(int).tolist()
            all_incomes = self.net_income
            npm = AST.calculate_net_profit_margin(total_revenues, all_incomes)
            return npm
        except Exception as e:
            print(f"Error with net_profit_margin {e}")
            return None

    @property
    def roe(self):
        try:
            all_incomes = self.net_income
            bal_df = pd.DataFrame(self.balance_sheet)

            total_assets = bal_df['totalAssets'].tolist()
            total_liabilities = bal_df['totalLiabilities'].tolist()
            years = pd.to_datetime(bal_df['fiscalDateEnding'])
            roe = AST.calculate_ROE(all_incomes, total_assets, total_liabilities, years)
            return roe
        except Exception as e:
            print(f"Error with roe: {e}")
            return None
