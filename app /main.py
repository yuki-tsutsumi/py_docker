from typing import Union
from apiUtil import ApiUtil
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/activate")
def get_activate():
    newActivate = ApiUtil()
    accessKey = newActivate.activate()
    return {"access_key": accessKey}