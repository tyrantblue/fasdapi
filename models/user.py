from models.base_db import TimeStampModel
from tortoise import fields
from passlib.context import CryptContext

# 创建一个密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(TimeStampModel):
    role: fields.ManyToManyRelation["Role"]  # type: ignore
    uid = fields.IntField(primary_key=True, description="用户id")
    username = fields.CharField(unique=True, max_length=50, description="用户名")
    hashed_password = fields.CharField(max_length=255, description="哈希后密码")
    nickname = fields.CharField(null=True, max_length=50, description="昵称")
    user_phone = fields.CharField(null=True, max_length=50, description="用户手机")
    user_email = fields.CharField(null=True, max_length=50, description="用户邮箱")
    user_status = fields.IntField(default=0, description="用户状态：-1无效，0启用，1禁用")
    image = fields.CharField(null=True, max_length=255, description="头像")
    client_host = fields.CharField(null=True, max_length=50, description="用户请求地址")

    async def verify_password(self, plan_password: str) -> bool:
        """校验密码"""
        return pwd_context.verify(plan_password, self.hashed_password)

    @staticmethod
    def get_hash_password(password: str) -> str:
        """
        获取哈希后的密码
        :param password: 明文密码
        """
        return pwd_context.hash(password)

    class Meta:  # 元
        table_description = "用户表"
        table = "user"
