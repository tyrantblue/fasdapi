from fastapi import Request, status
from fastapi.exceptions import HTTPException
from tortoise.exceptions import IntegrityError
from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from config import settings
from models import User
from schemas.user import UserIn
from core.utils import UserStatus


SECRET_KEY = settings.TOKEN_SECRET_KEY
ALGORITHM = settings.TOKEN_ALGORITHM


async def get_redis(request: Request):
    """
    注入redis连接到路由函数
    :param request:
    :return:
    """
    return request.app.state.redis


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """创建token

    Args:
        data (dict): 需要编码的信息
        expires_delta (Union[timedelta, None]): 设置过期时间. Defaults to None.

    Returns:
        str: 编码后的jwt令牌
    """
    to_decode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone(timedelta(hours=8))) + expires_delta
    else:
        expire = datetime.now(timezone(timedelta(hours=8))) + timedelta(minutes=15)
    to_decode.update({'exp': expire})
    encode_jwt = jwt.encode(to_decode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def create_user(user_info: UserIn) -> User:
    hash_password = User.get_hash_password(user_info.password)
    user_in = user_info.model_dump()
    user_in["hashed_password"] = hash_password
    user_in["user_status"] = UserStatus.USEFUL.value

    try:
        return await User.create(**user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="这个用户名已经被注册了，换一个吧，杂鱼。"
        )


async def authenticate_user(username: str, password: str) -> User:
    """
    校验用户和密码
    :param username:
    :param password:
    :return:
    """
    user = await User.get_or_none(username=username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到用户！")
    if not await user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误，杂鱼~",
        )
    return user
