from typing import Union,Optional
from app.apiUtil import ApiUtil
from fastapi import FastAPI,Cookie, File, UploadFile,Body
from app.database import db
from minio import Minio
import boto3
import shutil
from os.path import abspath
import os
import pika
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import json
from app.tasks import add

app = FastAPI()


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

@app.post("/files")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename,
            "contents": contents}

@app.post("/uploadfile/boto3")
async def create_upload_file_boto3(file: UploadFile = File(...)):
    # minioに接続
    s3 = boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id='root', #docker-compose:id
        aws_secret_access_key='password', # docker-compose:pass
    )
    
    # ファイルアップロード
    file_name = file.filename
    file_full_path = abspath(file_name)
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    s3.upload_file(file_full_path, "sample", file.filename)

    os.remove(file_full_path)
    return {"filename": file.filename}

@app.post("/uploadfile/minio")
async def create_upload_file_minio(file: UploadFile):
    contents = await file.read()

    # minioに接続
    s3 = Minio(
        endpoint='minio:9000',
        access_key='root', #docker-compose:id
        secret_key='password', # docker-compose:pass,
        secure=False
    )
    found = s3.bucket_exists("sample")
    if not found:
       s3.make_bucket("sample")

    s3.fput_object("sample", "sample.json","./sample.json",)

    return {"filename": file.filename,
            "contents": contents}

# RabbitMQ用
@app.get("/add-job/{message}")
def add_job(message: str):
    # RabbitMQサーバと接続（ホスト名にはコンテナ名を指定しているが，Dockerを使ってない場合はIPアドレスを指定）
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))
    # チャンネルの確立
    channel = connection.channel()
    # メッセージを格納するためのキュー(task_queue)を作成
    channel.queue_declare(queue="task_queue", durable=True)
    # メッセージをキュー(task_queue)に格納
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # メッセージの永続化
        ))
    # 接続のクローズ及びメッセージが配信されたことを確認
    connection.close()

    return {"send": message}

@app.post('/mongo/add')
def create_post(body=Body(...)):
    post = body['payload']
    print(post)
    db.posts.insert_one(post)
    return {'post': "ok"}

@app.get('/mongo/get')
def read_post():
    db_post = db.posts.find_one()
    return {'item': dumps(db_post)}

@app.put('/mongo/update')
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


# 受け取ったファイルをストレージ（minio）,キュー(rabbiymq),データベース(mongo)に格納
@app.post('/sample/recieve')
def sample_recieve(file: UploadFile = File(...)):
    api_util = ApiUtil()

    #ストレージにファイルをアップロード
    item_id_file_name = api_util.file_uploder(file)

    #キューにitem_idをアップロード
    api_util.queue_uploader()

    #データベースにitem_idを格納
    response = {"item_id":item_id_file_name}
    print(response)
    api_util.create_items(json.loads(json.dumps(response)))

    return response

# タスクで保存したデータをmonogdbから取得
@app.post('/celery/get')
def sample_celery():
    task_result = add.delay(22,88)
    print("=================== "+task_result.id)
    from time import sleep
    sleep(2)
    res = db.celery_taskmeta.find_one({"_id":task_result.id})
    return dumps(res)