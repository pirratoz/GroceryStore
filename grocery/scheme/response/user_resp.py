from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
)

from grocery.enums import UserRole


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole


class UserManyResponse(BaseModel):
    limit: int
    offset: int
    total: int
    users: list[UserResponse]
