
class Scopes:
    """
    作用域
    """
    # 用户查找
    USER_FIND_SELF = "user:find:self"  # 查看自己的信息
    USER_FIND_ALL = "user:find:all"  # 查看所有人的信息

    # 用户更新
    USER_UPDATE_SELF = "user:update:self"  # 更新自己的信息
    USER_UPDATE_ALL = "user:update:all"  # 更新所有人的信息

    # 用户删除
    USER_DELETE_SELF = "user:delete:self"  # 删除自己的账号
    USER_DELETE_ALL = "user:delete:all"  # 删除所有人的账号

    # 用户创建
    USER_CREATE_SELF = "user:create:self"  # 删除自己的账号

    # ... 其他权限 ...
