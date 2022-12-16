from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int,messege: str):
        self.status_code = status_code
        self.messege = messege

def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.messege})

def include_app(app):
	app.add_exception_handler(AppException, app_exception_handler)
