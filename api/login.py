import uuid

from fastapi import APIRouter
from pydantic import BaseModel, Field

login_router = APIRouter()


class LoginUser(BaseModel):
    username: str
    password: str


class SignUpUser(LoginUser):
    phone: str


@login_router.post('/login', summary="登录接口!!")
async def login(body: LoginUser):
    return body


@login_router.post('/signUp', summary="注册接口!!")
async def sign_up(body: SignUpUser):
    return body
