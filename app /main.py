from typing import Union,Optional
from apiUtil import ApiUtil
from fastapi import FastAPI,Cookie, File, UploadFile
from minio import Minio
import boto3
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
async def create_upload_file_boto3(file: UploadFile):
    contents = await file.read()

    # minioに接続
    s3 = boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id='root', #docker-compose:id
        aws_secret_access_key='password', # docker-compose:pass
    )

    # boto3.resourceでしか使えない
    # # 存在チェック
    # bucket = s3.Bucket('sample')
    # if not bucket.creation_date:
    #     s3.create_bucket(Bucket="sample")
    # # MinIOのバケット出力
    # print('バケット一覧')
    # for bucket in s3.buckets.all():
    #     print(bucket.name)
    
    # ファイルアップロード
    # POSTデータを入れる方法ができていない。
    s3.upload_file('./sample.json', "sample", file.filename)

    object_list = s3.list_objects(Bucket="sample").get("Contents")
    print(object_list)


    return {"filename": file.filename,
            "contents": contents}

@app.post("/uploadfile/minio")
async def create_upload_file_boto3(file: UploadFile):
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
