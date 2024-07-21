from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import UserRepository
from grocery.scheme.response import (
    UserManyResponse,
    UserResponse,
)


class UserGetAllUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def execute(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> UserManyResponse:
        total = await self.user_repo.get_count_records()
        users = await self.user_repo.get_all(
            limit=limit,
            offset=offset,
        )

        return UserManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            users=[
                UserResponse(**user.model_dump())
                for user in users
            ],
        )
