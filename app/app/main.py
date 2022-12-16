from fastapi import FastAPI
from app.api.api import api_router
from app.api.exception import app_exception

app = FastAPI()
app.include_router(api_router)
app_exception.include_app(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}