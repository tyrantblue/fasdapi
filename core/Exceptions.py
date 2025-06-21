from fastapi import HTTPException, Request, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Union

from pydantic import ValidationError


class UvicornException(Exception):
    """
    自定义服务器异常类
    """

    def __init__(self, code, err_msg, data=None, *args):
        if not data:
            data = {}
        self.code = code
        self.err_msg = err_msg
        self.data = data
        super().__init__(*args)


# 方案1: 使用同步函数（推荐）
def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
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


def add_exception_handler(application: FastAPI) -> None:
    application.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    application.add_exception_handler(RequestValidationError, http422_exception_handler)  # type: ignore
    application.add_exception_handler(UvicornException, uvicorn_exception_handler)  # type: ignore
