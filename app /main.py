from typing import Union
import redisService
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class RedisValue(BaseModel):
    key: str
    value: str

@app.post("/redis/add")
def sample_redis(body: RedisValue):
    redisService.setRedis(body)
    return {"status": "ok"}

@app.get("/redis/show/{key}")
def sample_redis(key: str):
    r = redisService.getRedis(key)
    return {"redis": r}