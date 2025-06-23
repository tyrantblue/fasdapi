# view路由汇总

from fastapi import APIRouter

from views.home import home_view


view_router = APIRouter(prefix='/view', tags=["view视图路由"])
view_router.include_router(home_view)




