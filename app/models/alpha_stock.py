import pandas as pd
from app.api.services.database_service_outputs import fetch_eps_from_database


class AlphaStock:
    def __init__(self, **kwargs):
        self.symbol = kwargs.get('symbol', None)
        self.income_statement = kwargs.get('income_statement', None)
        self.balance_sheet = kwargs.get('balance_sheet', None)
        self.annual_eps = kwargs.get('annual_eps', None)
        self.cash_flows = kwargs.get('cash_flows', None)
        self.co = kwargs.get('co', None)  # company overview
        self.market_data_info = kwargs.get('market_data', None)

    @property
    def revenue(self):
        try:
            df = pd.DataFrame(self.income_statement)
            df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding'])
            df['totalRevenue'] = pd.to_numeric(df['totalRevenue'], errors='coerce')
            df['growth_rate'] = df['totalRevenue'].pct_change() * 100  # Calculate and convert to percentage
            df['growth_rate'] = df['growth_rate'].fillna(0)

            data = df[['growth_rate', 'fiscalDateEnding']]

            return data

        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def debt(self):
        try:
            df = pd.DataFrame(self.balance_sheet)
            result = df[['currentDebt', 'fiscalDateEnding']]
            df['currentDebt'] = df['currentDebt'].fillna(0)

            return result
        except Exception as e:
            print(f"Error calculating debt level: {e}")
            return None

    @property
    def net_income(self):
        try:
            df = pd.DataFrame(self.income_statement)
            data = df[['fiscalDateEnding', 'netIncome']]
            return data
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def eps(self):
        try:
            df = pd.DataFrame(self.annual_eps)
            data = df[['fiscalDateEnding', 'reportedEPS']]
            return data
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    @property
    def net_profit_margin(self):
        try:
            df_income = pd.DataFrame(self.income_statement)
            df_income['netProfitMargin'] = (pd.to_numeric(df_income['netIncome'], errors='coerce') / pd.to_numeric(
                df_income['totalRevenue'], errors='coerce')) * 100

            df_income['netProfitMargin'] = df_income['netProfitMargin'].pct_change() * 100

            net_profit = df_income[['netProfitMargin', 'fiscalDateEnding']]

            return net_profit
        except Exception as e:
            print(f"Error with net_profit_margin {e}")
            return None

    @property
    def roe(self):
        try:
            income_df = pd.DataFrame(self.income_statement)
            bal_df = pd.DataFrame(self.balance_sheet)

            bal_df['shareholdersEquity'] = (pd.to_numeric(bal_df['totalAssets'], errors='coerce') - pd.to_numeric(
                bal_df['totalLiabilities'], errors='coerce'))
            bal_df['roe'] = (pd.to_numeric(income_df['netIncome'], errors='coerce') - bal_df['shareholdersEquity'])

            roe = bal_df[['fiscalDateEnding', 'roe']]
            return roe

        except Exception as e:
            print(f"Error with roe: {e}")
            return None

    @property
    def cash(self):
        try:
            cf = pd.DataFrame(self.cash_flows.get('annualReports'))
            result = cf[['fiscalDateEnding', 'operatingCashflow']]
            return result
        except Exception as e:
            print(f"Error with cash method: {e}")
            return None

    @property
    def fcf(self):
        try:
            cf = pd.DataFrame(self.cash_flows.get('annualReports'))
            ebitda = float(self.co['EBITDA'])
            tax = self.tax_rate
            capex = float(cf.iloc[0]['capitalExpenditures'])

            fcf = ebitda * (1 - tax) - capex

            return fcf
        except Exception as e:
            print(f"Error calculating free cash flows: {e}")
            return None

    @property
    def dcf(self):
        try:
            projection_years = 5
            dcf = (self.fcf + self.terminal_value / (1 + self.discount_rate) ** projection_years)
            return dcf
        except Exception as e:
            print(f"Error calculating discounted cash flows: {e}")
            return None

    @property
    def growth_rate(self):
        try:
            info = fetch_eps_from_database(self.symbol)
            years = info[1]
            eps = info[0]
            eps_start = eps[0][0]
            eps_end = eps[-1][0]
            years = len(years) - 1  # Number of full years between the first and last EPS value
            ca_gr = (eps_end / eps_start) ** (1 / years) - 1
            return ca_gr # compound annual growth rate
        except Exception as e:
            print(f"Error calculating growth rate: {e}")
            return None

    @property
    def tax_rate(self):
        try:
            df = pd.DataFrame(self.income_statement)
            tax = float(df['incomeTaxExpense'].iloc[0]) / float(df['incomeBeforeTax'].iloc[0])
            return tax
        except Exception as e:
            print(f"Error calculating tax rate: {e}")
            return None

    @property
    def discount_rate(self):
        try:
            ratios = self.calculate_ratios
            risk_rate = 0.03  # Hardcoded value
            market_return = self.calculate_market_data
            beta = float(self.co['Beta'])
            cost_of_debt = self.calculate_cost_of_debt
            debt_ratio = ratios[0]
            equity_ratio = ratios[1]
            total_market_value = equity_ratio + debt_ratio
            cost_of_equity = risk_rate + beta * (market_return - risk_rate)
            tax_rate = self.tax_rate

            wacc = (equity_ratio / total_market_value) * cost_of_equity + (
                    debt_ratio / total_market_value) * cost_of_debt * (1 - tax_rate)
            return wacc
        except Exception as e:
            print(f"Error calculating discount rate: {e}")
            return None

    @property
    def calculate_ratios(self):
        try:
            b_df = pd.DataFrame(self.balance_sheet)
            total_debt = float(b_df['totalLiabilities'].iloc[0])
            total_equity = float(b_df['totalShareholderEquity'].iloc[0])
            debt_ratio = total_debt / (total_debt + total_equity)
            equity_ratio = total_equity / (total_debt + total_equity)
            return debt_ratio, equity_ratio
        except Exception as e:
            print(f"Error calculating debt and/or equity ratio: {e} ")
            return None

    @property
    def calculate_cost_of_debt(self):
        try:
            i_df = pd.DataFrame(self.income_statement)
            b_df = pd.DataFrame(self.balance_sheet)

            interest_expense = float(i_df['interestExpense'].iloc[0])
            total_debt = float(b_df['totalLiabilities'].iloc[0])
            cost_of_debt = interest_expense / total_debt
            return cost_of_debt
        except Exception as e:
            print(f"Error calculating cost of debt: {e}")
            return None

    @property
    def terminal_value(self):
        try:
            terminal_growth_rate = 0.03
            discount_rate = self.discount_rate

            terminal_value = self.fcf * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
            return terminal_value
        except Exception as e:
            print(f"Error calculating terminal value: {e}")
            return None

    @property
    def calculate_market_data(self):
        try:
            self.market_data_info['daily_return'] = self.market_data_info['Adj Close'].pct_change()
            average_market_return = self.market_data_info['daily_return'].mean() * 252

            return average_market_return
        except Exception as e:
            print(f"Error calculating market data: {e}")
            return None

    @property
    def calculate_intrinsic_value(self):
        try:
            dcf = self.dcf
            so = float(self.co['SharesOutstanding'])
            return dcf / so
        except Exception as e:
            print(f"Error calculating intrinsic value : {e}")
            return None
