from grocery.scheme.response import ProductManyResponse
from grocery.repositories import ProductRepository
from grocery.usecases.base_uc import BaseUseCase


class ProductGetAllUseCase(BaseUseCase):
    def __init__(self, product_repo: ProductRepository) -> None:
        self.product_repo = product_repo

    async def execute(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> ProductManyResponse:
        ...
