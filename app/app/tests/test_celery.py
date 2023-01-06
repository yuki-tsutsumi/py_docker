from fastapi.testclient import TestClient
from app.api.model.plus import Plus
from app.database import db
from bson.objectid import ObjectId

from app.main import app

client = TestClient(app)

def test_read_celery_正常系():
    a_num = 10
    b_num = 10
    json = {
        "a": a_num,
        "b": b_num
    }
    plus = Plus(**json)
    response = client.post("/celery/get_mongo_data",json=plus.dict())
    assert response.status_code == 200
    assert response.json()["result"] == str(a_num+b_num)
    dbid = response.json()["_id"]
    db_result = db.celery_taskmeta.find_one({"_id":dbid})
    assert db_result
