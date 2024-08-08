from app.api.services.unknown_services import get_the_list_from_the_db
from fastapi import  APIRouter

unknown_router = APIRouter(prefix='/unknown')
@unknown_router.get('/')
async def list_of_stocks(symbol:str):

    try:
        # Fetch the stock data
        stock = yf.Ticker(symbol)

        # Get the stock info
        stock_info = stock.info

        # Extract the P/E Ratio
        pe_ratio = stock_info.get('forwardEps') and stock_info.get('forwardPE')

        if pe_ratio:
            return pe_ratio
        else:
            print(f"P/E Ratio not found for {symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching P/E Ratio for {symbol}: {e}")
        return None

