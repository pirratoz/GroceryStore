from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Body,
)

from grocery.scheme.response import TokenResponse
from grocery.dependencies import SessionReadOnly
from grocery.repositories import UserRepository
from grocery.usecases.user_auth_uc import UserAuthUseCase
from grocery.scheme.request import UserAuthRequest


jwt = APIRouter()


@jwt.post("/auth")
async def auth(
    user_data: Annotated[UserAuthRequest, Body],
    session: SessionReadOnly = Depends()
) -> TokenResponse:
    token = await UserAuthUseCase(
        user_repo=UserRepository(session)
    ).execute(user_data)
    return token
