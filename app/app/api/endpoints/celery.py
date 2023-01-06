from fastapi import APIRouter
from app.database import db
from app.tasks import add
from app.api.model.plus import Plus

router = APIRouter()

# タスクで保存したデータをmonogdbから取得
@router.post('/get_mongo_data')
def sample_celery(plus:Plus):
    task_result = add.delay(plus.dict()["a"],plus.dict()["b"])
    from time import sleep
    sleep(0.5)
    res = db.celery_taskmeta.find_one({"_id":task_result.id})
    return res