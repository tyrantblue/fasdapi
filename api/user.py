from typing import List
from tortoise.exceptions import DoesNotExist
from fastapi import APIRouter, Depends, status
from models import User
from schemas.user import UserOut, UserUpdate
from api.dependencies import create_user
from core.response import success, fail, ResponseModel


user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get('/all', response_model=ResponseModel[List[UserOut]])
async def get_all_user():
    """
    获取全部用户
    :return:
    """
    users: List[User] = await User.all()
    return success(data=users)


@user_router.get('/{user_id}', response_model=ResponseModel[UserOut])
async def get_one_user(user_id: int):
    """
    根据ID获取用户信息
    :param user_id: 用户id
    :return:
    """
    user = await User.get_or_none(uid=user_id)

    if not user:
        return fail(message="用户不存在，你的查询参数是不是有问题？", code=status.HTTP_404_NOT_FOUND)

    return success(data=user)


@user_router.post('/', response_model=ResponseModel[UserOut])
async def create_user(user_out: User = Depends(create_user)):
    """
    创建用户
    :param user_out: 返回的用户信息
    :return:
    """
    return await user_out


@user_router.put('/{user_id}', response_model=ResponseModel[UserOut])
async def update_user(user_id: int, user_update: UserUpdate):
    """
    更新用户信息。
    :param user_id: 需要更新的用户ID
    :param user_update: 需要更新的用户信息
    :return:
    """
    user = await User.get_or_none(uid=user_id)

    if not user:
        return fail(message="想更新一个不存在的用户？你的逻辑呢？", code=status.HTTP_404_NOT_FOUND)

    updated_user = user_update.model_dump(exclude_unset=True)
    await user.update_from_dict(updated_user)
    await user.save()
    return success(data=user)


@user_router.delete('/{user_id}', response_model=ResponseModel[UserOut])
async def delete_user(user_id: int):
    """
    删除用户
    :param user_id:
    :return:
    """
    try:
        user = await User.get(uid=user_id)
        await user.delete()
    except DoesNotExist:
        return fail(message="用户都不存在，你还想删除什么？", code=status.HTTP_404_NOT_FOUND)
    return success(data=user)
