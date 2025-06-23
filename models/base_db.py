from tortoise import Model, fields

# print("!!! Module models.base_db is being imported !!!")  # 验证此包是否被导入


class TimeStampModel(Model):
    """
    数据时间模型
    """
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True  # 作为抽象基类不生成表
