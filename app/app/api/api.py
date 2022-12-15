from fastapi import APIRouter

from app.api.endpoints import item
from app.api.endpoints import activate
from app.api.endpoints import uploadfile
from app.api.endpoints import sample
from app.api.endpoints import mongo
from app.api.endpoints import celery

api_router = APIRouter()

api_router.include_router(item.router)
api_router.include_router(activate.router)
api_router.include_router(uploadfile.router)
api_router.include_router(sample.router)
api_router.include_router(mongo.router)
api_router.include_router(celery.router)