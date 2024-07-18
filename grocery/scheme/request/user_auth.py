from pydantic import (
    BaseModel,
    EmailStr,
)


class UserAuthRequest(BaseModel):
    email: EmailStr
    password: str
