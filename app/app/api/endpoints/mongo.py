from fastapi import APIRouter
from fastapi import Body
from app.database import db
from bson.json_util import dumps
from bson.objectid import ObjectId

router = APIRouter()

@router.post('/add')
def create_post(body=Body(...)):
    post = body['payload']
    print(post)
    db.posts.insert_one(post)
    return {'post': "ok"}

@router.get('/get')
def read_post():
    db_post = db.posts.find_one()
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