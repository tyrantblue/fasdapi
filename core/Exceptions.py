from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from typing import Union, Awaitable
import asyncio

from pydantic import ValidationError


class UvicornException(Exception):
    """
    自定义服务器异常类
    """

    def __init__(self, code, err_msg, data=None, *args, **kwargs):
        if not data:
            data = {}
        self.code = code
        self.err_msg = err_msg
        self.data = data
        super().__init__(*args, **kwargs)


# 方案1: 使用同步函数（推荐）
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    自定义http异常处理（同步版本）
    :param request: Request对象
    :param exc: HTTPException异常
    :return: JSONResponse
    """
    return JSONResponse(
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": exc.detail
        },
        status_code=exc.status_code
    )


def http422_exception_handler(request: Request, exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    """
    自定义http参数验证异常处理（同步版本）
    :param request: Request对象
    :param exc: 验证异常
    :return: JSONResponse
    """
    return JSONResponse(
        content={
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": f"参数校验错误：{exc.errors()}",
            "data": exc.errors()
        },
        status_code=422
    )


def uvicorn_exception_handler(request: Request, exc: UvicornException) -> JSONResponse:
    """
    自定义UvicornException异常处理（同步版本）
    """
    return JSONResponse(
        content={
            "code": exc.code,
            "message": exc.err_msg,
            "data": exc.data
        },
        status_code=exc.code if 100 <= exc.code <= 599 else 500
    )


# 方案3: 使用装饰器方式创建异步处理器
def create_async_http_exception_handler():
    async def handler(request: Request, exc: HTTPException) -> JSONResponse:
        # 异步操作示例
        # await some_async_logging_function(exc)
        return JSONResponse(
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": exc.detail
            },
            status_code=exc.status_code
        )
    return handler


def create_async_http422_exception_handler():
    async def handler(request: Request, exc: Union[RequestValidationError, ValidationError]) -> Response:
        # 异步操作示例
        # await some_async_logging_function(exc)
        return JSONResponse(
            content={
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": f"参数校验错误：{exc.errors()}",
                "data": exc.errors()
            },
            status_code=422
        )
    return handler


def create_async_uvicorn_exception_handler():
    async def handler(request: Request, exc: UvicornException) -> Response:
        """
        自定义UvicornException异常处理（同步版本）
        """
        return JSONResponse(
            content={
                "code": exc.code,
                "message": exc.err_msg,
                "data": exc.data
            },
            status_code=exc.code if 100 <= exc.code <= 599 else 500
        )
    return handler
