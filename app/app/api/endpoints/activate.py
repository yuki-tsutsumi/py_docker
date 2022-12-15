from fastapi import APIRouter
from typing import Optional
from app.apiUtil import ApiUtil
from fastapi import Cookie

router = APIRouter()

@router.post("/")
def get_activate(accesskey: Optional[str] = Cookie(None)):
    newActivate = ApiUtil()
    accessKeyVal = newActivate.activate(accesskey)
    return {"access_key": accessKeyVal}
