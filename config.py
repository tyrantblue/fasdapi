import os.path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any
from pydantic import SecretStr


class Config(BaseSettings):
    # 调试模式
    APP_DEBUG: bool = True
    # 项目信息
    VERSION: str = "0.0.1"
    PROJECT_NAME: str = "FasdAPI"
    PROJECT_DESCRIPTION: str = "FasdAPI"
    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    # 视图目录
    TEMPLATES_DIR: str = os.path.join(os.getcwd(), "templates")
    # 跨域请求
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    # session
    SESSION_SECRET_KEY: str = "YOUR KEY."
    SESSION_SESSION_COOKIE: str = "session"
    SESSION_MAX_AGE: int = 10


class RedisSettings(BaseSettings):
    """
    redis设置类
    """
    model_config = SettingsConfigDict(env_prefix='REDIS_', env_file=".env", extra="ignore")
    host: str
    port: int
    encoding: str = 'utf-8'
    username: str = ''
    password: SecretStr = SecretStr('')
    db: int = 0
    decode_responses: bool = True

    @property
    def redis_config(self) -> Dict[str, Any]:
        """
        获取redis的连接设置
        :return:
        """
        return {
            "url": f"redis://{self.username}:{self.password.get_secret_value()}"
                   f"@{self.host}:{self.port}"
                   f"/{self.db}",
            "decode_responses": self.decode_responses
        }


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BASE_DB_', env_file=".env", extra="ignore")
    host: str
    port: int
    username: str
    password: SecretStr
    database_name: str


class TortoiseSettings(BaseSettings):
    base_db: DatabaseSettings = DatabaseSettings()

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
                "base_db": f"mysql://{self.base_db.username}:{self.base_db.password.get_secret_value()}"
                           f"@{self.base_db.host}:{self.base_db.port}"
                           f"/{self.base_db.database_name}"
            },
            "apps": self.tortoise_apps,
            "use_timezone": self.use_timezone,
            "timezone": self.timezone
        }


settings = Config()  # 框架基础设置

redis_settings = RedisSettings()  # redis设置

tortoise_settings = TortoiseSettings()  # tortoise数据库设置
