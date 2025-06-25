from fastapi import FastAPI, applications
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from config import settings
from core.middlewares import add_middleware_handler
from core.events import lifespan
from core.exceptions import add_exception_handler
from core.router import all_router
from core.utils import swagger_monkey_patch


# 国内访问swagger
applications.get_swagger_ui_html = swagger_monkey_patch


# 1. 创建FastAPI实例，设置生命周期
application = FastAPI(
    debug=settings.APP_DEBUG,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# 2. 添加异常处理器（使用异步版本）
add_exception_handler(application)

# 3. 注册路由
application.include_router(all_router)

# 4. 注册中间件 (不要写错了关键字）
add_middleware_handler(application)

# 5. 挂载静态文件
application.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# 6. 在请求头中增加
application.state.views = Jinja2Templates(directory=settings.TEMPLATES_DIR)  # type: ignore

app = application
