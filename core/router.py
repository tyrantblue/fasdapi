# 路由汇总
from fastapi import APIRouter
from api.base import API_router
from views.base import view_router

all_router = APIRouter()

# api路由实例导入
all_router.include_router(API_router)
# view路由实例导入
all_router.include_router(view_router)
