from fastapi import Request


async def get_redis(request: Request):
    """
    注入redis连接到路由函数
    :param request:
    :return:
    """
    return request.app.state.redis
