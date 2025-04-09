import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import MutableHeaders

from controllers import users, auth
from config import main_settings, auth_settings
from authx.exceptions import MissingTokenError, CSRFError, JWTDecodeError
from sqlalchemy.exc import IntegrityError

app = FastAPI()
app.include_router(auth.route)
app.include_router(users.route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def update_csrf_headers(request: Request, call_next):
    """ Дублирование CSRF-токена из cookies в headers, если он есть
    иначе security.access_token_required не увидит csrf-токен """
    if auth_settings.JWT_ACCESS_CSRF_COOKIE_NAME in request.cookies:
        new_headers = MutableHeaders(request.headers)
        new_headers[auth_settings.JWT_ACCESS_CSRF_HEADER_NAME] = request.cookies[
            auth_settings.JWT_ACCESS_CSRF_COOKIE_NAME]
        request.scope.update(headers=new_headers.raw)
    return await call_next(request)


@app.exception_handler(MissingTokenError)
@app.exception_handler(CSRFError)
@app.exception_handler(JWTDecodeError)
async def validation_exception_handler(request: Request, ex: Exception):
    """ Ошибки Authx"""
    raise HTTPException(status_code=403, detail=str(ex))


@app.exception_handler(IntegrityError)
async def validation_exception_handler(request: Request, ex: Exception):
    """ Ошибка postgresql """
    msg = ex.args[0].split("DETAIL:  ")[1]
    raise HTTPException(status_code=400, detail=msg)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=main_settings.PORT, reload=main_settings.DEBUG)
