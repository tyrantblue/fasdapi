from core.security import create_access_token, TokenPayload
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api.dependencies import create_user, authenticate_user
from models import User
from schemas.user import UserOut
from core.response import success, fail, ResponseModel

login_router = APIRouter(tags=["login"])


@login_router.post("/login", summary="账号密码登录接口")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    登录，返回token
    :param form_data:
    :return:
    """
    # 1. 验证 form_data.username 和 form_data.password
    try:
        user = await authenticate_user(form_data.username, form_data.password)
    except HTTPException as e:
        return fail(message=e.detail, code=e.status_code)

    # 2. 创建Token
    access_token = await create_access_token(TokenPayload(**{"uid": user.uid}))
    # 3. 把Token直接返回给客户端！不是塞进session！
    return success(data={"access_token": access_token, "token_type": "bearer"})


@login_router.post('/register', summary="注册接口!!", response_model=ResponseModel[UserOut])
async def sign_up(body: User = Depends(create_user)):
    return success(data=body)
