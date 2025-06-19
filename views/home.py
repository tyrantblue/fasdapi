"""

"""
from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse
from typing import Optional
from models.base_db import User

home_view = APIRouter(prefix="/home", tags=["主页视图"])


@home_view.get("/register", response_class=HTMLResponse)
async def register(request: Request) -> HTMLResponse:
    """
    注册页面
    :param request: 请求
    :return: HTMLResponse
    """
    return request.app.state.views.TemplateResponse("home/register.html", {"request": request})


@home_view.post("/result", response_class=HTMLResponse)
async def index(request: Request, username: str = Form(), password: str = Form()) -> HTMLResponse:
    """
    结果界面
    :param request: 请求
    :param username: 用户名
    :param password: 密码
    :return:
    """
    print(await User().all())
    print(await User().create(username=username, password=password))
    print(await User().all())
    res: dict = {
        "request": request,
        "data": {
            "username": username,
            "password": password,
        }
    }
    return request.app.state.views.TemplateResponse("home/result.html", res)


@home_view.get("/cookie", response_class=HTMLResponse)
async def cookie_view(request: Request) -> HTMLResponse:
    """
    结果界面
    :param request: 请求
    :param cookie:
    :return:
    """

    res: dict = {
        "request": request,
        "data": {
            "session": str(request.session),
        }
    }
    request.session["session_1"] = "session_1"
    request.session["session_2"] = "session_2"
    print(request.session)
    return request.app.state.views.TemplateResponse("home/cookie.html", res)
