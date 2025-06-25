import jwt
from datetime import datetime, timedelta
from fastapi import Depends, Path
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List

from config import settings
from models import Access, Role
from core.scopes import Scopes

SECRET_KEY = settings.TOKEN_SECRET_KEY
ALGORITHM = settings.TOKEN_ALGORITHM


# 这就是那个“门卫”的定义, tokenUrl明确说了从哪个地方拿到token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# 1. 定义你的Token载荷模型，这就是编码和解码的“规则”！
class TokenPayload(BaseModel):
    """
    Token载荷模型
    """
    uid: int
    exp: int = int((datetime.now() + timedelta(days=28)).timestamp())  # 28天失效
    token_scopes: List[Optional[str]] = []  # 获取的权限
    is_gm: bool = False


async def create_access_token(token_payload: TokenPayload):
    """创建token

    Args:
        token_payload: token包含的信息

    Returns:
        str: 编码后的jwt令牌
    """
    to_decode = token_payload.model_dump()
    encode_jwt = jwt.encode(to_decode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    【基础依赖】: 只负责解码token，并从数据库获取用户完整信息（权限、角色等）
    它不进行任何针对特定接口的权限校验！
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="token 验证失败！",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception
    try:
        print(token)
        token_payload_data = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except ValueError as e:
        raise credentials_exception
    except Exception as e:
        raise credentials_exception

    # 验证时间已过则失效
    if token_payload_data["exp"] < int(datetime.now().timestamp()):
        raise credentials_exception

    # 先查询redis缓存中的数据（还未有实现）

    # 无则查询数据库中的数据

    # 用户为超管则不进行验证
    is_gm = True if await Role.get_or_none(id=1, user__uid=token_payload_data["uid"]) else False

    # 查数据库，获取该用户的所有权限
    user_scopes = []

    if not is_gm:
        # 非超管才需要查具体权限
        scope_records = await Access.filter(
            role__user__uid=token_payload_data["uid"],
            role__user__user_status=0,
            role__role_status=True
        ).values_list("scope", flat=True)
        user_scopes = list(scope_records)

    token_payload_data['is_gm'] = is_gm
    token_payload_data['token_scopes'] = user_scopes
    # 组装成一个完整的、信息丰富的 TokenPayload 对象！
    return TokenPayload(
        **token_payload_data
    )


def require_scopes(*required_scopes: str):
    """
    【验证器工厂】: 依赖于基础依赖，用于验证普通权限。
    """

    async def _verify_scopes(
            user: TokenPayload = Depends(get_current_active_user)
    ):
        # 1. 是超管？直接放行！
        if user.is_gm:
            return user

        # 2. 不是超管，检查是否拥有所有必需的权限
        if all([scope not in user.token_scopes for scope in required_scopes]):
            raise HTTPException(status_code=403, detail=f"权限不足！")

        return user

    return _verify_scopes


def require_user_access(all_scope: str, self_scope: str):
    """
    【验证器工厂】: 用于验证“自己 vs 所有人”这种复杂场景。
    """

    async def _verify_access(
            target_user_id: int = Path(...),
            # 同样，依赖于纯净的数据提供者！
            operator: TokenPayload = Depends(get_current_active_user)
    ):
        # 1. 是超管？直接放行！
        if operator.is_gm:
            return operator

        # 2. 有操作所有人的权限？放行！
        if all_scope in operator.token_scopes:
            return operator

        # 3. 只有操作自己的权限，并且正在操作自己？放行！
        if self_scope in operator.token_scopes and operator.uid == target_user_id:
            return operator

        # 4. 其它情况？滚蛋！
        raise HTTPException(status_code=403, detail="权限不足！无法对该用户执行此操作。")

    return _verify_access


require_update_user = require_user_access(Scopes.USER_UPDATE_ALL, Scopes.USER_UPDATE_SELF)
require_delete_user = require_user_access(Scopes.USER_DELETE_ALL, Scopes.USER_DELETE_SELF)
require_find_user = require_user_access(Scopes.USER_FIND_ALL, Scopes.USER_FIND_SELF)
