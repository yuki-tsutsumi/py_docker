from fastapi import APIRouter,HTTPException
from fastapi import Body
from app.database import db
from bson.json_util import dumps
from bson.objectid import ObjectId
from app.api.exception.app_exception import AppException

router = APIRouter()

@router.post('/add')
def create_post(body=Body(...)):
    post = body['payload']
    db.posts.insert_one(post)
    return {'post': "ok"}

@router.get('/get/list')
def read_post():
    db_post = db.posts.find()
    return {'item': dumps(db_post)}

@router.get('/get/{id}')
def read_one_post(id:str):
    db_post = db.posts.find_one({"_id":ObjectId(id)})
    if not db_post:
        raise AppException(201,"NOT_FOUND_DATA")
    return {'item': dumps(db_post)}

@router.put('/update')
def update_post(body=Body(...)):
    post = body['payload']
    _id = post['_id']
    title = post['title']
    text = post['text']
    db.posts.update_one(
        {'_id': ObjectId(_id)},
        {'$set':
            {
                "title": title, 'text': text
            }
        }
    )
    return {'update': "ok"}