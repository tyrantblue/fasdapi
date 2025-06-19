from fastapi import FastAPI
from database.mysql import init_tortoise
from database.redis import init_redis, close_redis


def start_up(app: FastAPI):
    async def app_start():
        # 使用aioredis 连接redis
        app.state.redis = await init_redis()
        # 使用tortoise-orm 连接mysql
        await init_tortoise(app)
        print("启动完毕！！")

    return app_start


def stopping(app: FastAPI):

    async def app_stop():
        await close_redis(app.state.redis)
        print("程序停止！！")

    return app_stop
