from fastapi import HTTPException

from grocery.scheme.request import UserAuthRequest
from grocery.scheme.response import TokenResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import UserRepository
from grocery.utils import (
    Password,
    Jwt,
)


class UserAuthUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def execute(self, user_data: UserAuthRequest) -> TokenResponse:
        user = await self.user_repo.get_user_by_email(user_data.email)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Email or password incorrect"
            )
        
        if not Password.verify(user_data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Email or password incorrect"
            )
        
        token = Jwt.encode(
            {
                "id": str(user.id),
                "role": user.role.value
            }
        )

        return TokenResponse(
            access_token=token,
            token_type="Bearer"
        )