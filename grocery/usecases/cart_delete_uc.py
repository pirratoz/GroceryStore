from uuid import UUID

from grocery.repositories import CartRepository
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import CartClearResponse


class CartDeleteUseCase(BaseUseCase):
    def __init__(self, cart_repo: CartRepository) -> None:
        self.cart_repo = cart_repo

    async def execute(self, user_id: UUID) -> CartClearResponse:
        result = await self.cart_repo.clear_all(user_id)
        return CartClearResponse(cleared=result)
