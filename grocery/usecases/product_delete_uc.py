from uuid import UUID

from fastapi import HTTPException

from grocery.scheme.response import ProductResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.dependencies import MinIoClient
from grocery.utils import ImageUrlsTool
from grocery.repositories import (
    ProductRepository,
    ImageRepository,
)


class ProductDeleteUseCase(BaseUseCase):
    def __init__(
        self,
        product_repo: ProductRepository,
        image_repo: ImageRepository,
    ) -> None:
        self.product_repo = product_repo
        self.image_repo = image_repo

    async def execute(self, id: UUID, clientS3: MinIoClient) -> ProductResponse:        
        product = await self.product_repo.get_one_by_id(id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if (image := await self.image_repo.get_one_by_id(product.image_id)):
            await self.image_repo.delete_by_id(product.image_id)
            await ImageUrlsTool.delete(clientS3, image.filename)

        await self.product_repo.delete_by_id(id)

        return ProductResponse.get_model(product)
