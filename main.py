import uvicorn
from fastapi import FastAPI

from app.api.routers.ML_router import ML_router
from app.api.routers.auth_router import auth_router
from app.api.routers.calculators_router import stock_calculator
from app.api.routers.company_router import company_router
from app.api.routers.core_stock_router import stocks_router
from app.api.routers.news_router import news_router
from app.api.routers.unknown_router import unknown_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(unknown_router)
app.include_router(news_router, tags=['News'])
app.include_router(auth_router, tags=['Authentication'])
app.include_router(stocks_router, tags=['Stocks'])
app.include_router(stock_calculator, tags = ['Calculators'])
app.include_router(ML_router, tags = ['ML'])
app.include_router(company_router, tags=['Company'])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


