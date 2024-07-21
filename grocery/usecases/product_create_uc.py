from fastapi import HTTPException

from grocery.scheme.request import ProductCreateRequest
from grocery.scheme.response import ProductResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import (
    SubCategoryRepository,
    ProductRepository,
    ImageRepository,
)


class ProductCreateUseCase(BaseUseCase):
    def __init__(
        self,
        subcategory_repo: SubCategoryRepository,
        product_repo: ProductRepository,
        image_repo: ImageRepository
    ) -> None:
        self.subcategory_repo = subcategory_repo
        self.product_repo = product_repo
        self.image_repo = image_repo

    async def execute(self, data: ProductCreateRequest) -> ProductResponse:        
        product = await self.product_repo.get_one_by_slug(data.slug)
        if product:
            raise HTTPException(
                status_code=409,
                detail="Slug is not unique"
            )
        
        subcategory = await self.subcategory_repo.get_one_by_id(data.subcategory_id)
        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail="SubCategory not found"
            )
        
        image = await self.image_repo.get_one_by_id(data.image_id)
        if not image:
            raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

        product = await self.product_repo.create(
            subcategory_id=data.subcategory_id,
            title=data.title,
            slug=data.slug,
            image_id=data.image_id,
            price=data.price,
            weight_gramm=data.weight_gramm
        )
        product = await self.product_repo.get_one_by_id(product.id)

        return ProductResponse.get_model(product)
