from tortoise import Model, fields


class User(Model):
    id = fields.IntField(primary_key=True, description="用户id")
    username = fields.CharField(max_length=50, description="用户名")
    password = fields.CharField(max_length=50, description="密码")
    nickname = fields.CharField(null=True, max_length=50, description="昵称")
    user_phone = fields.CharField(null=True, max_length=50, description="用户手机")
    user_email = fields.CharField(null=True, max_length=50, description="用户邮箱")
    user_status = fields.IntField(default=0, max_length=50, description="用户状态：0启用，1禁用")
    image = fields.CharField(null=True, max_length=255, description="头像")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    client_host = fields.CharField(null=True, max_length=50, description="用户请求地址")
