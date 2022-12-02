from typing import Union,Optional
from apiUtil import ApiUtil
from fastapi import FastAPI,Cookie, File, UploadFile

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
