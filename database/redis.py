from aioredis import Redis
import aioredis
from config import redis_settings
from typing import Union


async def init_redis() -> Union[Redis, None]:
    """
    初始化Redis
    :return: Redis实例
    """
    print(f"Redis 正在连接...")
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        url=redis_settings.redis_config["url"],
        decode_responses=redis_settings.redis_config["decode_responses"]
    )
    try:
        redis_client = Redis(connection_pool=sys_cache_pool)
        await redis_client.ping()
        print("Redis 连接成功！")
        return redis_client
    except Exception as e:
        print(f"Redis 连接失败，Error: {e}")
    return None


async def close_redis(redis_client: Redis) -> None:
    if not redis_client:
        print("Redis 已提前关闭")
        return None

    print("Redis 正在关闭...")
    await redis_client.close()
    print("Redis 已关闭！")
