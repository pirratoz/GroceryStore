from fastapi.responses import JSONResponse
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


@cart.post("/")
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


@cart.delete("/")
async def delete_cart(
    auth: Auth = Depends(),
    session: Session = Depends()
) -> CartClearResponse:
    await CartDeleteUseCase(
        cart_repo=CartRepository(session)
    ).execute(auth["id"])
    return JSONResponse(content={}, status_code=204)
