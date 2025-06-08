# 工具函数

import hashlib
import uuid
from fastapi.openapi.docs import get_swagger_ui_html


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

