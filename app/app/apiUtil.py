import uuid
import json
import redis
from fastapi import HTTPException,status
import boto3
import os
import shutil
from os.path import abspath
import pika
from app.database import db
from app.api.exception.app_exception import AppException
from bson.json_util import dumps
from bson.objectid import ObjectId

class ApiUtil:

    kvs = redis.Redis(host=os.environ.get("KVS_HOST"), port=os.environ.get("KVS_PORT"), db=0)

    EXPIRE = 60*60
    REDIS_KEY_ID = "id"
    accessKey = None

    # minioに接続
    s3 = boto3.client(
        's3',
        endpoint_url=os.environ.get("MINIO_SERVER_URL"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), #docker-compose:id
        aws_secret_access_key=os.environ.get("AWS_SEACRET_ACCESS_KEY"), # docker-compose:pass
    )

    item_id = None

    def activate(self,cookieVal):
        if self.getAccessKey(cookieVal) and self.getRedis(self.REDIS_KEY_ID):
            raise HTTPException(status_code=status.HTTP_200_OK,detail=f"USER_ALREADY_ACTIVATED ")
        accessKey = str(uuid.uuid4())
        redisVal = {'id':''}
        self.setAccessKey(accessKey)
        self.setRedis(self.REDIS_KEY_ID,json.dumps(redisVal),self.EXPIRE)
        return accessKey
    
    def getAccessKey(self,cookieVal):
        if self.accessKey == None:
            self.accessKey = cookieVal
        return self.accessKey

    def setAccessKey(self,accessKey):
        self.accessKey = accessKey

    # Redisに情報を保存する
    def setRedis(self,keyPrefix, value, expire = 60):
        key = keyPrefix + '::' + self.accessKey
        self.kvs.set(key, value)
        self.kvs.expire(key, expire)

    # Redisから情報を取得する
    def getRedis(self,keyPrefix,expire = 60):
        key = keyPrefix + '::' + self.accessKey
        value = self.kvs.get(key)
        if value:
            self.kvs.expire(key, expire) 
        return value

    # ファイルをminioにアップロードする
    def file_uploder(self,file):
        self.item_id = str(uuid.uuid4())
        item_id_file_name = self.item_id+"_"+file.filename
        file_full_path = abspath(item_id_file_name)
        with open(item_id_file_name, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        self.s3.upload_file(file_full_path, "sample", item_id_file_name)

        os.remove(file_full_path)

        return item_id_file_name

    # メッセージをrabbitMQにアップロードする
    def queue_uploader(self):
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
            body=self.item_id+"_recieved",
            properties=pika.BasicProperties(
                delivery_mode=2,  # メッセージの永続化
            ))
        # 接続のクローズ及びメッセージが配信されたことを確認
        connection.close()
    
    def create_items(self,item):
        db.items.insert_one(item)
    
    def getOne(self,id:str):
        db_post = db.posts.find_one({"_id":ObjectId(id)})
        if not db_post:
            raise AppException(201,"NOT_FOUND_DATA")
        return {'item': dumps(db_post)}

