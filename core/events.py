from fastapi import FastAPI
from database.redis import init_redis, close_redis


def start_up(app: FastAPI):
    async def app_start():
        # 使用aioredis 连接redis
        app.state.redis = await init_redis()  # type: ignore
        print("启动完毕！！")

    return app_start


def stopping(app: FastAPI):

    async def app_stop():
        # 结束redis连接
        await close_redis(app.state.redis)  # type: ignore
        print("程序停止！！")

    return app_stop
