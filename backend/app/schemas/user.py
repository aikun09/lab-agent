from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """用户信息响应参数"""

    id: int
    username: str
    name: str
    role: str
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    status: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):
    """更新用户信息的请求参数"""

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None


class PasswordUpdateRequest(BaseModel):
    """修改密码的请求参数"""

    old_password: str
    new_password: str
