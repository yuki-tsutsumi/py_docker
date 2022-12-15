from fastapi import APIRouter
from fastapi import File, UploadFile
from minio import Minio
import boto3
import shutil
from os.path import abspath
import os

router = APIRouter(
    prefix='/uploadfile',
    tags=['uploadfile']
)

@router.post("/files")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@router.post("/uploadfiles")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename,
            "contents": contents}

@router.post("/boto3")
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

@router.post("/minio")
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