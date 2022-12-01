from typing import Union,Optional
from apiUtil import ApiUtil
from fastapi import FastAPI,Cookie
from middleware import AuthActivateMiddleware
app = FastAPI()

# ミドルウェアは作ることがができたが、ルーティングを変更できず、activateに
# ミドルウェアが走ってしまう。
# app.add_middleware(AuthActivateMiddleware)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/activate")
def get_activate(accesskey: Optional[str] = Cookie(None)):
    newActivate = ApiUtil()
    accessKeyVal = newActivate.activate(accesskey)
    return {"access_key": accessKeyVal}