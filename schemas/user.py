from pydantic import BaseModel, Field
from typing import Optional


# 创建用户时的输入模型
class UserIn(BaseModel):
    username: str = Field(..., max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    user_status: Optional[int] = Field(None, description="用户状态")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    user_email: Optional[str] = Field(None, max_length=50, description="用户邮箱")


# 响应给客户端的用户模型，绝对不能包含密码！
class UserOut(BaseModel):
    uid: int
    username: str
    nickname: Optional[str]
    user_email: Optional[str]
    user_status: int
    image: Optional[str]
    user_status: Optional[int]

    class Config:
        from_attributes = True  # 从 ORM 模型自动转换，这点小方便就留给你吧


# 更新用户时的输入模型，所有字段都是可选的
class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    user_email: Optional[str] = Field(None, max_length=50, description="用户邮箱")
    user_status: Optional[int] = Field(None, description="用户状态")
    image: Optional[str] = Field(None, max_length=255, description="头像")
