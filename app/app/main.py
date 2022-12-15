from fastapi import FastAPI

from app.router import item
from app.router import activate
from app.router import uploadfile
from app.router import sample
from app.router import mongo
from app.router import celery

app = FastAPI()
app.include_router(item.router)
app.include_router(activate.router)
app.include_router(uploadfile.router)
app.include_router(sample.router)
app.include_router(mongo.router)
app.include_router(celery.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}