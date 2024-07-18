from uuid import UUID

from pydantic import EmailStr

from grocery.dto.base_dto import BaseModelDto
from grocery.enums import UserRole


class UserDto(BaseModelDto):
    id: UUID
    email: EmailStr
    password: bytes
    role: UserRole
