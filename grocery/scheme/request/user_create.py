from pydantic import (
    BaseModel,
    EmailStr,
)

from grocery.enums import UserRole


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: bytes
    role: UserRole
