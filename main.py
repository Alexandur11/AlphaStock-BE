import uvicorn
from fastapi import FastAPI

from app.api.routers.login_router import logout_router, login_router
from app.api.routers.register_router import register_router

app = FastAPI()


app.include_router(register_router)
app.include_router(login_router)
app.include_router(logout_router)
@app.post('/')
def home():
    return 'hello'
# app.include_router(login_router, tags=[LOGIN_REGISTER])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)