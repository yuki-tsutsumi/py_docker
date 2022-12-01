from fastapi import Request,HTTPException,status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from apiUtil import ApiUtil

class AuthActivateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):        
        newActivate = ApiUtil()
        cookie = request.cookies.get("accesskey")
        if cookie is None or newActivate.getRedis(cookie) is None:
            return JSONResponse(status_code=401, content={'detail': str("ACCESSKEY_UNAUTHORIZED")})


        response = await call_next(request)
        return response