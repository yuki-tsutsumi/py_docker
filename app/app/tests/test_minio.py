from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
import boto3
import os
from pathlib import Path
import tempfile
import pytest

from app.main import app

client = TestClient(app)

# minioに接続
s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get("MINIO_SERVER_URL"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SEACRET_ACCESS_KEY"),
)

# tempフォルダにアップロード用一時ファイルを作成
def create_tmp_file(suffix,contents):
    fd, path = tempfile.mkstemp(prefix='test-', suffix=suffix)
    with open(path, 'w+') as f:
        f.write(contents)
        f.seek(os.SEEK_SET)

    # ファイル名のみ取り出す
    name = path.split('/')[-1]
    return {"name":name,"path":path}

@pytest.fixture(params=[
    ('.json', '{"test":"test"}'), 
    ('.text', "test"), 
    ('.png', "aaaaaaaaaaaaaaaa")
])
def file_context(request):
    return (request.param[0], request.param[1])

def test_read_minio_テキスト_正常系(file_context):
    tmp_file = create_tmp_file(file_context[0],file_context[1])
    name = tmp_file["name"]
    path = tmp_file["path"]

    upload_file = Path(path)
    files = {'file': upload_file.open('rb')}

    # tmpファイルを展開したので削除
    os.unlink(path)

    response = client.post("/uploadfile/boto3",files=files)
    assert response.status_code == 200
    assert response.json()["filename"] == name
    # minioにファイルが格納されているか
    exists = s3.get_object(Bucket='sample',Key=name)
    assert exists

    # minioのデータを削除
    s3.delete_object(Bucket='sample',Key=name)