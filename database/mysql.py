from typing import Any, Dict

import yaml
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from tortoise.contrib.fastapi import register_tortoise


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BASE_DB_', env_file=".env", extra="ignore")
    host: str
    port: int
    username: str
    password: str
    database_name: str


class Settings(BaseSettings):
    base_db: DBSettings = SettingsConfigDict(env_file=".env", extra="ignore")

    tortoise_apps: Dict[str, Any] = {
        "main_model": {
            "models": ["models.base_db"],
            "default_connection": "base_db"
        }
    }
    use_timezone: bool = False
    timezone: str = "Asia/Shanghai"

    @property
    def tortoise_orm_config(self) -> Dict[str, Any]:
        return {
            "connections": {
                "base_db": f"mysql://{self.base_db.username}:{self.base_db.password}@{self.base_db.host}:{self.base_db.port}/{self.base_db.database_name}"
            },
            "apps": self.tortoise_apps,
            "use_timezone": self.use_timezone,
            "timezone": self.timezone
        }


def init_db(app: FastAPI) -> None:
    """
    初始化数据库
    :return:
    """

    settings = Settings()
    print(f"tortoise_orm_config: {settings}")
    register_tortoise(
        app,
        config=settings.tortoise_orm_config,
        generate_schemas=True,
        add_exception_handlers=True,
    )
