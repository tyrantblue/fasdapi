from fastapi import FastAPI, applications
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from config import settings
from database.mysql import init_tortoise
from core.middlewares import add_middleware_handler
from core.events import stopping, start_up
from core.exceptions import add_exception_handler

from core.router import all_router
from core.utils import swagger_monkey_patch


# 国内访问swagger
applications.get_swagger_ui_html = swagger_monkey_patch


application = FastAPI(
    debug=settings.APP_DEBUG,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
)

# 1. 初始化数据库
init_tortoise(application)

# 2. 添加事件处理器
application.add_event_handler("startup", start_up(application))
application.add_event_handler("shutdown", stopping(application))

# 3. 添加异常处理器（使用异步版本）
add_exception_handler(application)

# 4. 注册路由
application.include_router(all_router)


# 5. 注册中间件 (不要写错了关键字）
add_middleware_handler(application)


# 6. 挂载静态文件
application.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# 7. 在请求头中增加
application.state.views = Jinja2Templates(directory=settings.TEMPLATES_DIR)  # type: ignore


app = application
