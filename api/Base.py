# api部分路由汇总

from fastapi import APIRouter
from api.login import login_router


API_router = APIRouter(prefix="/api", tags=["api接口"])
API_router.include_router(login_router)

# 这种方式耦合度太高了
# API_router.post('/login')(login)
