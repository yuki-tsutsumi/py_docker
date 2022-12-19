from fastapi import APIRouter,HTTPException
from fastapi import Body
from app.database import db
from bson.json_util import dumps
from bson.objectid import ObjectId
from app.api.exception.app_exception import AppException
from app.apiUtil import ApiUtil
from app.api.model.payload import Payload,Posts

router = APIRouter()

@router.post('/add')
def create_post(payload:Payload):
    document = payload.dict()['payload']
    post_id = db.posts.insert_one(document).inserted_id
    return {'post': str(post_id)}

@router.get('/get/list')
def read_post():
    db_post = db.posts.find()
    return {'item': dumps(db_post)}

@router.get('/get/{id}')
def read_one_post(id:str):
    api_util = ApiUtil()
    db_post = api_util.getOne(id)
    return db_post

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