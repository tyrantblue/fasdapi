# view路由汇总

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse


view_router = APIRouter(prefix='/view', tags=["view视图路由"])


@view_router.get("/index", response_class=HTMLResponse)
async def index(request: Request, uid: int):
    return request.app.state.views.TemplateResponse("index.html", {"request": request, "uid": uid})

