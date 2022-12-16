from fastapi import APIRouter
from app.apiUtil import ApiUtil
from fastapi import File, UploadFile
import pika
import json

router = APIRouter()

# RabbitMQ用
@router.get("/{message}")
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

# 受け取ったファイルをストレージ（minio）,キュー(rabbiymq),データベース(mongo)に格納
@router.post('/recieve')
def sample_recieve(file: UploadFile = File(...)):
    api_util = ApiUtil()

    #ストレージにファイルをアップロード
    item_id_file_name = api_util.file_uploder(file)

    #キューにitem_idをアップロード
    api_util.queue_uploader()

    #データベースにitem_idを格納
    response = {"item_id":item_id_file_name}
    api_util.create_items(json.loads(json.dumps(response)))

    return response