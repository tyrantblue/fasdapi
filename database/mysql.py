
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import tortoise_settings


async def init_tortoise(app: FastAPI) -> None:
    """
    初始化数据库
    :return:
    """

    print(f"mysql 正在连接...")
    register_tortoise(
        app,
        config=tortoise_settings.tortoise_orm_config,
        generate_schemas=True,
        add_exception_handlers=True,
    )
