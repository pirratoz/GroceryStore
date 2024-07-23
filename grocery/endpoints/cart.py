from fastapi.responses import Response
from fastapi import (
    APIRouter,
    Depends,
)

from grocery.dependencies import (
    SessionReadOnly,
    Session,
    Auth,
)
from grocery.repositories import (
    CartRepository,
)
from grocery.usecases import (
    CartDeleteUseCase,
    CartCreateUseCase,
    CartGetUseCase,
)
from grocery.scheme.request import (
    CartCreateRequest,
)
from grocery.scheme.response import (
    CartClientResponse,
    CartClearResponse,
    CartResponse,
)


cart = APIRouter()


@cart.get("/")
async def get_cart(
    auth: Auth = Depends(),
    session: SessionReadOnly = Depends()
) -> CartClientResponse:
    cart = await CartGetUseCase(
        cart_repo=CartRepository(session)
    ).execute(
        user_id=auth["id"]
    )
    return cart


@cart.post(
    path="/",
    status_code=201
)
async def create_cart(
    data: CartCreateRequest,
    auth: Auth = Depends(),
    session: Session = Depends()
) -> CartResponse | CartClearResponse:
    cart = await CartCreateUseCase(
        cart_repo=CartRepository(session)
    ).execute(
        user_id=auth["id"],
        data=data
    )
    return cart


@cart.delete(
    path="/",
    status_code=204,
)
async def delete_cart(
    auth: Auth = Depends(),
    session: Session = Depends()
) -> Response:
    await CartDeleteUseCase(
        cart_repo=CartRepository(session)
    ).execute(auth["id"])
    return Response(status_code=204)
