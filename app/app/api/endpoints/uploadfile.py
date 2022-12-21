from fastapi import APIRouter,HTTPException
from fastapi import File, UploadFile
from minio import Minio
import boto3
import shutil
from os.path import abspath
import os

router = APIRouter()

@router.post("/files")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@router.post("/uploadfiles")
async def create_upload_file(file: UploadFile):
    if file.content_type != 'application/json':
        raise HTTPException(422,"Other application/json type is not usage file")
    contents = await file.read()
    return {"filename": file.filename,
            "contents": contents}

@router.post("/boto3")
async def create_upload_file_boto3(file: UploadFile = File(...)):
    # minioに接続
    s3 = boto3.client(
        's3',
        endpoint_url=os.environ.get("MINIO_SERVER_URL"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SEACRET_ACCESS_KEY"),
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
        endpoint=os.environ.get("MINIO_SERVER_DOMAIN"),
        access_key=os.environ.get("AWS_ACCESS_KEY_ID"), #docker-compose:id
        secret_key=os.environ.get("AWS_SEACRET_ACCESS_KEY"), # docker-compose:pass,
        secure=False
    )
    found = s3.bucket_exists("sample")
    if not found:
       s3.make_bucket("sample")

    s3.fput_object("sample", "sample.json","./sample.json",)

    return {"filename": file.filename,
            "contents": contents}