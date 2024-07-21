from fastapi import HTTPException

from grocery.scheme.request import UserCreateRequest
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import UserResponse
from grocery.repositories import UserRepository
from grocery.utils import Password


class UserCreateUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def execute(self, user_data: UserCreateRequest) -> UserResponse:
        user = await self.user_repo.get_user_by_email(user_data.email)

        if user is None:
            user = await self.user_repo.create(
                email=user_data.email,
                password=Password.create(user_data.password.decode("utf-8")),
                role=user_data.role,
            )
            return UserResponse.model_validate(user.model_dump())

        raise HTTPException(
            status_code=409,
            detail="User Already exists"
        )
