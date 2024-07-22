from uuid import UUID

from fastapi import HTTPException

from grocery.scheme.request import ProductPartialUpdateRequest
from grocery.scheme.response import ProductResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import (
    SubCategoryRepository,
    ProductRepository,
    ImageRepository,
)


class ProductPartialUpdateUseCase(BaseUseCase):
    def __init__(
        self,
        subcategory_repo: SubCategoryRepository,
        product_repo: ProductRepository,
        image_repo: ImageRepository
    ) -> None:
        self.subcategory_repo = subcategory_repo
        self.product_repo = product_repo
        self.image_repo = image_repo

    async def execute(
        self,
        product_id: UUID,
        data: ProductPartialUpdateRequest
    ) -> ProductResponse:
        
        if data.subcategory_id:
            subcategory = await self.subcategory_repo.get_one_by_id(data.subcategory_id)
            if not subcategory:
                raise HTTPException(
                    status_code=404,
                    detail="SubCategory not found"
                )
        
        if data.image_id:
            image = await self.image_repo.get_one_by_id(data.image_id)
            if not image:
                raise HTTPException(
                    status_code=404,
                    detail="Image not found"
                )

        if data.slug:
            product = await self.product_repo.get_one_by_slug(data.slug)
            if product:
                raise HTTPException(
                    status_code=409,
                    detail="Slug is not unique"
                )

        product = await self.product_repo.update_partial(
            id=product_id,
            kwargs=data.model_dump(exclude_none=True)
        )

        return ProductResponse.get_model(product)
