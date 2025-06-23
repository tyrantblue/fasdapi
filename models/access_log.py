from models.base_db import TimeStampModel
from tortoise import fields


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
