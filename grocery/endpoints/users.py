from fastapi import (
    APIRouter,
    Depends,
)

from grocery.scheme.request import UserCreateRequest
from grocery.repositories import UserRepository
from grocery.scheme.response import (
    UserManyResponse,
    UserResponse,
)
from grocery.dependencies import (
    SessionReadOnly,
    Session,
    Auth,
)
from grocery.usecases import (
    UserCreateUseCase,
    UserGetAllUseCase,
)

users = APIRouter()


@users.get("/", dependencies=[Depends(Auth.auth)])
async def get_users(
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> UserManyResponse:
    users = await UserGetAllUseCase(
        user_repo=UserRepository(session)
    ).execute(limit=limit, offset=offset)
    return users


@users.post("/", status_code=201)
async def create_user(
    user_data: UserCreateRequest,
    session: Session = Depends()
) -> UserResponse:
    user = await UserCreateUseCase(
        user_repo=UserRepository(session)
    ).execute(user_data)
    return user
