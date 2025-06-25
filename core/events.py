from fastapi import FastAPI
from database.redis import init_redis, close_redis
from database.tortoise_orm import init_tortoise, close_tortoise
from contextlib import asynccontextmanager


async def start_up(app: FastAPI):

    # 使用tortoise 连接数据库
    await init_tortoise()
    # 使用aioredis 连接redis
    app.state.redis = await init_redis()  # type: ignore
    print("启动完毕！！")


async def stopping(app: FastAPI):

    # 结束tortoise连接
    await close_tortoise()
    # 结束redis连接
    await close_redis(app.state.redis)  # type: ignore
    print("程序停止！！")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    生命周期
    :return:
    """
    await start_up(app)
    yield
    await stopping(app)
