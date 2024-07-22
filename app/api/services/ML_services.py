from ML_Stock_Predictor.stock_predictor import stock_predictor
from app.api.fetches.stock_fetches import stock_monthly_adjusted
import pandas as pd


def ml_stock_prediction(stock):
    data = stock_monthly_adjusted(stock)
    info = pd.DataFrame(data['Monthly Adjusted Time Series'])
    return stock_predictor(info)
