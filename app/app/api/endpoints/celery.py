from fastapi import APIRouter
from app.database import db
from bson.json_util import dumps
from app.tasks import add

router = APIRouter(
    prefix='/celery',
    tags=['celery']
)

# タスクで保存したデータをmonogdbから取得
@router.post('/get')
def sample_celery():
    task_result = add.delay(22,88)
    print("=================== "+task_result.id)
    from time import sleep
    sleep(2)
    res = db.celery_taskmeta.find_one({"_id":task_result.id})
    return dumps(res)