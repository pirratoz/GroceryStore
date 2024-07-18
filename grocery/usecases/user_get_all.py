from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories.user_repo import UserRepository
from grocery.scheme.response.user_resp import (
    UserManyResponse,
    UserResponse,
)


class UserGetAllUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def execute(self, limit: int, offset: int) -> UserManyResponse:
        total = await self.user_repo.get_count_record()
        users = await self.user_repo.get_users_by_offset(
            limit=limit,
            offset=offset,
        )
        return UserManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            users=[
                UserResponse(id=user.id, email=user.email, role=user.role)
                for user in users
            ],
        )
