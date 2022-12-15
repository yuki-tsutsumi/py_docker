from fastapi import APIRouter

from app.api.endpoints import item
from app.api.endpoints import activate
from app.api.endpoints import uploadfile
from app.api.endpoints import sample
from app.api.endpoints import mongo
from app.api.endpoints import celery

api_router = APIRouter()

api_router.include_router(item.router,prefix='/item',tags=['item'])
api_router.include_router(activate.router,prefix='/activate',tags=['activate'])
api_router.include_router(uploadfile.router,prefix='/uploadfile',tags=['uploadfile'])
api_router.include_router(sample.router,prefix='/sample',tags=['sample'])
api_router.include_router(mongo.router,prefix='/mongo',tags=['mongo'])
api_router.include_router(celery.router,prefix='/celery',tags=['celery'])