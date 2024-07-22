from fastapi import HTTPException

from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import ProductResponse
from grocery.repositories import (
    SubCategoryRepository,
    CategoryRepository,
    ProductRepository,
)


class CatalogGetProductUseCase(BaseUseCase):
    def __init__(
        self,
        category_repo: CategoryRepository,
        subcategory_repo: SubCategoryRepository,
        product_repo: ProductRepository,
    ) -> None:
        self.category_repo = category_repo
        self.subcategory_repo = subcategory_repo
        self.product_repo = product_repo

    async def execute(
        self,
        slug_category: str,
        slug_subcategory: str,
        slug_product: str
    ) -> ProductResponse:
        category = await self.category_repo.get_one_by_slug(slug_category)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )
        
        subcategory = await self.subcategory_repo.get_one_by_slug(slug_subcategory)
        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail="SubCategory not found"
            )
        
        product = await self.product_repo.get_one_by_slug(slug_product)
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return ProductResponse.get_model(product)
