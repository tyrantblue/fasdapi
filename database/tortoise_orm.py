
from tortoise import Tortoise
from config import tortoise_settings
from models import User, Role


async def init_tortoise() -> None:
    """
    初始化数据库
    :return:
    """
    # 1. 连接数据库
    print(f"mysql 正在连接...")
    await Tortoise.init(
        config=tortoise_settings.tortoise_orm_config
    )
    print(f"mysql 连接成功！\n正在自动创建表...")
    await Tortoise.generate_schemas()

    # 2. 创建超管角色
    print(f"创建表成功！\n正在创建管理员账号...")
    root_role, created = await Role.get_or_create(
        role_name="SuperAdmin",
        defaults={
            "role_status": True,
            "role_desc": "超级管理员角色",
            "is_protected": True
        }
    )
    if created:
        print(f"角色 '{root_role.role_name}' 已创建！")

    # 3. 创建超管用户，uid=1
    root_user, created = await User.get_or_create(
        uid=1,
        defaults={
            "username": "root",
            "nickname": "root",
            "hashed_password": User.get_hash_password("123456"),
            "user_status": 0
        }
    )

    await root_user.role.add(root_role)

    print(f"用户 '{root_user.username}' (uid=1) 已创建并设为超级管理员！")
    print("数据库初始化完成！")


async def close_tortoise() -> None:
    """
    数据库连接关闭
    :return:
    """
    await Tortoise.close_connections()
