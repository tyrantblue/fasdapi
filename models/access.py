from models.base_db import TimeStampModel
from tortoise import fields


class Access(TimeStampModel):
    role: fields.ManyToManyRelation["Role"]  # type: ignore
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

