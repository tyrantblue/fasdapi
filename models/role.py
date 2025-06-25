from models.base_db import TimeStampModel
from tortoise import fields


class Role(TimeStampModel):
    """
    角色模型
    """
    role_name = fields.CharField(max_length=50, description="角色名称")
    user: fields.ManyToManyRelation["User"] = (    # type: ignore
        fields.ManyToManyField("main_model.User", related_name="role", on_delete=fields.CASCADE)
    )
    access: fields.ManyToManyRelation["Access"] = (    # type: ignore
        fields.ManyToManyField("main_model.Access", related_name="role", on_delete=fields.CASCADE)
    )
    role_status = fields.BooleanField(default=False, description="True: 启用; False: 禁用")
    role_desc = fields.CharField(default=None, max_length=255, description="角色描述")
    is_protected = fields.BooleanField(default=False, description="是否被保护角色，True则不可删除/修改")

    class Meta:
        table = "role"
        table_description = "角色表"
