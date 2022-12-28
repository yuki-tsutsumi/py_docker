from fastapi.testclient import TestClient
from app.database import db
from bson.json_util import dumps
from app.api.model.payload import Payload
from bson.objectid import ObjectId

from app.main import app

client = TestClient(app)

# mongomockは使わない
# import mongomock
# def get_client():
#     BACKEND_URL = "%s://%s:%s@%s:%d/%s" % (
#     os.environ.get("MONGO_DATABASE_PROTOCOL"),os.environ.get("MONGO_DATABASE_USER"),
#     os.environ.get("MONGO_DATABASE_PASSWORD"), os.environ.get("MONGO_DATABASE_HOST"), 
#     int(os.environ.get("MONGO_DATABASE_PORT")), os.environ.get("MONGO_DATABASE_NAME"))

#     return mongomock.MongoClient(BACKEND_URL)

def test_read_mongo_get_id():
    dbid =  db.posts.insert_one({"name": "foo", "age": 20}).inserted_id
    url="/mongo/get/"+str(dbid)
    response = client.get(url)
    post = db.posts.find_one({"_id":dbid})
    assert response.json()['item'] == dumps(post)

def test_read_mongo_add_正常系():
    json = {
        "payload": {
            "title": "string",
            "text": 10
        }
    }
    payload = Payload(**json)
    url="/mongo/add"
    response = client.post(url,json=payload.dict())
    add_id = response.json()["post"]
    assert len(add_id) == 24
    result = db.posts.find_one({"_id":ObjectId(add_id)})
    assert result["title"] == "string"
    assert result["text"] == 10