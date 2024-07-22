from uuid import UUID

from grocery.repositories import CartRepository
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import CartClientResponse


class CartGetUseCase(BaseUseCase):
    def __init__(self, cart_repo: CartRepository) -> None:
        self.cart_repo = cart_repo

    async def execute(
        self,
        user_id: UUID
    ) -> CartClientResponse:
        response = await self.cart_repo.get_client_cart(user_id=user_id)
        return CartClientResponse.get_model(response)
