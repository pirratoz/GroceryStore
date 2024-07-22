from grocery.repositories import ProductRepository
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import (
    ProductManyResponse,
    ProductResponse,
)


class ProductGetAllUseCase(BaseUseCase):
    def __init__(self, product_repo: ProductRepository) -> None:
        self.product_repo = product_repo

    async def execute(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> ProductManyResponse:
        total = await self.product_repo.get_count_records()
        products = await self.product_repo.get_all(
            limit=limit,
            offset=offset,
        )

        return ProductManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            products=[
                ProductResponse.get_model(product)
                for product in products
            ]
        )
