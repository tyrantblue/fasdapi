from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from models.base_db import User
from typing import List, Optional

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get('/people')
async def get_user(request: Request):
    """
    获取用户
    :param request:
    :return:
    """

