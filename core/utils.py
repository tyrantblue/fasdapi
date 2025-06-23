# 工具函数
import hashlib
import uuid
from fastapi.openapi.docs import get_swagger_ui_html
from enum import Enum


class UserStatus(Enum):
    """
    User状态枚举类
    """
    INVALID: int = -1  # 无效
    USEFUL: int = 0  # 可用
    UNUSEFUL: int = -1  # 不可用


def random_str() -> str:
    """
    唯一随机字符串
    :return: str
    """
    only = hashlib.md5(str(uuid.uuid1()).encode('utf-8')).hexdigest()
    return str(only)


def swagger_monkey_patch(*args, **kwargs):
    """
    国内访问swagger
    :param args:
    :param kwargs:
    :return:
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")


if __name__ == '__main__':
    # print(create_access_token({"test": "test"}))
    print(0 == UserStatus.USEFUL.value)
    print(UserStatus.USEFUL)
    print(UserStatus.USEFUL.value)
    # print(UserStatus.USEFUL is 0)
