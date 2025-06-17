from fastapi import FastAPI, HTTPException, applications
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.datastructures import State
from starlette.middleware.sessions import SessionMiddleware

from config import settings
from core.Events import stopping, start_up
from core.Middleware import MyMiddleware
from core.Exceptions import (
    create_async_http_exception_handler,
    create_async_http422_exception_handler,
    create_async_uvicorn_exception_handler,
    UvicornException,
)

from core.Router import all_router
from core.Helper import swagger_monkey_patch

from database.mysql import init_db


class CustomState(State):
    """
    可以继承自Starlette.datastructures，不继承也行
    """
    views: Jinja2Templates


class CreateFastAPI(FastAPI):
    """
    固定state属性防止编辑器警告，不写也行
    """
    state: CustomState


# 国内访问swagger
applications.get_swagger_ui_html = swagger_monkey_patch


application = CreateFastAPI(
    debug=settings.APP_DEBUG,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
)


# 添加事件处理器
application.add_event_handler("startup", start_up(application))
application.add_event_handler("shutdown", stopping(application))


# 添加异常处理器（使用异步版本）
application.add_exception_handler(HTTPException, create_async_http_exception_handler())
application.add_exception_handler(RequestValidationError, create_async_http422_exception_handler())
application.add_exception_handler(UvicornException, create_async_uvicorn_exception_handler())


# 路由
application.include_router(all_router)


# 中间件 (不要写错了关键字）
application.add_middleware(MyMiddleware)  # type: ignore
application.add_middleware(
        SessionMiddleware,  # type: ignore
        secret_key=settings.SESSION_SECRET_KEY,
        session_cookie=settings.SESSION_SESSION_COOKIE,
        # max_age=4
)
application.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# 挂载静态文件
application.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# 添加请求头
application.state.views = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# 使用tortoise-orm 连接数据库
init_db(application)

app = application

