from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse


# 定义一个泛型，你这种杂鱼大脑能理解什么叫泛型吗？
T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """
    标准响应模型
    """
    code: int = Field(200, description="业务状态码, 200-成功")
    message: str = Field("Success", description="响应消息")
    data: Optional[T] = None  # data 字段是可选的，并且可以是任何类型 T

# --- 下面是两个方便你这种脑子转不过弯的人使用的快捷工厂函数 ---


def success(data: Optional[T] = None, message: str = "Success") -> ResponseModel[T]:
    """
    成功响应的快捷方式
    哼，就是帮你把 data 塞进去而已，这么简单还要我教？
    """
    return ResponseModel(data=data, message=message)


def fail(message: str, code: int = 400) -> JSONResponse:
    """
    失败响应的快捷方式
    注意！这里直接返回一个 JSONResponse 对象，这样才能自定义 HTTP 状态码！
    别傻乎乎地直接返回一个 Pydantic 模型，HTTP 状态码默认可是 200 OK！
    一个失败的业务逻辑，怎么能返回 200 OK 呢？你的逻辑处理器不会报错吗？！
    """
    error_response = ResponseModel(code=code, message=message, data=None)
    return JSONResponse(
        status_code=code,  # 这里设置真正的 HTTP 状态码
        content=error_response.model_dump()
    )