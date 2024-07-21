from fastapi import HTTPException

from grocery.scheme.request import UserCreateRequest
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import UserResponse
from grocery.repositories import UserRepository
from grocery.utils import PasswordTools


class UserCreateUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def execute(self, user_data: UserCreateRequest) -> UserResponse:
        user = await self.user_repo.get_one_by_email(user_data.email)

        if user:
            raise HTTPException(
                status_code=409,
                detail="User Already exists"
            )

        user = await self.user_repo.create(
            email=user_data.email,
            password=PasswordTools.create(user_data.password.decode("utf-8")),
            role=user_data.role,
        )

        return UserResponse(**user.model_dump())

