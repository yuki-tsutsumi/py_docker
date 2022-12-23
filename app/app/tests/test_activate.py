from fastapi.testclient import TestClient
import os
import redis
from app.apiUtil import ApiUtil

from app.main import app

client = TestClient(app)

kvs = redis.Redis(host=os.environ.get("KVS_HOST"), port=os.environ.get("KVS_PORT"), db=0)

def test_activate_no_cookie():
    response = client.post("/activate")
    assert response.status_code == 200
    assert response.json()["access_key"] != None
    accesskey = response.json()["access_key"]
    redis_accesskey = ApiUtil.REDIS_KEY_ID + "::" + accesskey
    assert kvs.exists(redis_accesskey) == True

def test_activate_has_cookie():
    response = client.post("/activate")
    accesskey = response.json()["access_key"]
    client.cookies = {"accesskey":accesskey}
    response = client.post("/activate")
    assert response.status_code == 200
    assert response.json()["detail"] == "USER_ALREADY_ACTIVATED"
    redis_accesskey = ApiUtil.REDIS_KEY_ID + "::" + accesskey
    assert kvs.exists(redis_accesskey) == True


