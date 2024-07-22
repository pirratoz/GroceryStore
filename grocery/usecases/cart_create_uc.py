from uuid import UUID

from grocery.scheme.response import (
    CartClearResponse,
    CartResponse,
)
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import CartRepository
from grocery.scheme.request import CartCreateRequest


class CartCreateUseCase(BaseUseCase):
    def __init__(
        self,
        cart_repo: CartRepository
    ) -> None:
        self.cart_repo = cart_repo

    async def execute(
        self,
        user_id: UUID,
        data: CartCreateRequest,
    ) -> CartResponse | CartClearResponse:
        cart = await self.cart_repo.check_in_cart(user_id, data.product_id)
        if cart and data.count <= 0:
            result = await self.cart_repo.delete_by_id(cart_id=cart.id)
            return CartClearResponse(cleared=result)
        
        if cart is None:
            cart = await self.cart_repo.create(
                user_id=user_id,
                product_id=data.product_id,
                count=data.count
            )
        else:
            cart = await self.cart_repo.update_partial(
                cart_id=cart.id,
                user_id=cart.user_id,
                product_id=cart.product_id,
                count=cart.count
            )
        return CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            product_id=cart.product_id,
            count=data.count
        )
