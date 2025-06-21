from tortoise import Model, fields
# print("!!! Module models.base_db is being imported !!!")  # 验证此包是否被导入


# class Test(Model):
#     id = fields.IntField(pk=True)
#     content = fields.TextField()


class TimeStampModel(Model):
    """
    数据时间模型
    """
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = None


class User(TimeStampModel):
    role: fields.ManyToManyRelation["Role"]
    id = fields.IntField(primary_key=True, description="用户id")
    username = fields.CharField(max_length=50, description="用户名")
    password = fields.CharField(max_length=50, description="密码")
    nickname = fields.CharField(null=True, max_length=50, description="昵称")
    user_phone = fields.CharField(null=True, max_length=50, description="用户手机")
    user_email = fields.CharField(null=True, max_length=50, description="用户邮箱")
    user_status = fields.IntField(default=0, max_length=50, description="用户状态：0启用，1禁用")
    image = fields.CharField(null=True, max_length=255, description="头像")
    client_host = fields.CharField(null=True, max_length=50, description="用户请求地址")

    class Meta:  # 元
        table_description = "用户表"
        table = "user"


class Access(TimeStampModel):
    role: fields.ManyToManyRelation["Role"]
    rule_name = fields.CharField(max_length=15, description="权限名称")
    parent_id = fields.IntField(description="父亲ID")
    scopes = fields.CharField(unique=True, max_length=255, description="权限作用域")
    rule_desc = fields.CharField(null=True, max_length=255, description="权限描述")
    menu_icon = fields.CharField(null=True, max_length=255, description="菜单图标")
    is_check = fields.BooleanField(default=False, description="是否验证权限 True: 验证; False: 不验证")
    is_menu = fields.BooleanField(default=False, description="是否为菜单 True: 是; False: 不是")

    class Meta:
        table_description = "权限表"
        table = "access"


class Role(TimeStampModel):
    """
    角色模型
    """
    role_name = fields.CharField(max_length=50, description="角色名称")
    user: fields.ManyToManyRelation["User"] = (
        fields.ManyToManyField("main_model.User", related_name="role", on_delete=fields.CASCADE)
    )
    access: fields.ManyToManyRelation["Access"] = (
        fields.ManyToManyField("main_model.Access", related_name="role", on_delete=fields.CASCADE)
    )
    role_status = fields.BooleanField(default=False, description="True: 启用; False: 禁用")
    role_desc = fields.CharField(default=None, max_length=255, description="角色描述")

    class Meta:
        table = "role"
        table_description = "角色表"


class AccessLog(TimeStampModel):
    user_id = fields.IntField(description="用户ID")
    target_url = fields.CharField(null=True, max_length=255, description="访问的url")
    user_agent = fields.CharField(null=True, max_length=255, description="用户ID")
    request_params = fields.JSONField(null=True, description="请求参数get|post")
    ip = fields.CharField(null=True, max_length=255, description="访问IP")
    note = fields.CharField(null=True, max_length=255, description="备注")

    class Meta:
        table_description = "用户操作记录表"
        table = "access_log"
