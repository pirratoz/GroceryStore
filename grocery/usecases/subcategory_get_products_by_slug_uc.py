from fastapi import HTTPException

from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import (
    ProductManyResponse,
    ProductResponse,
)
from grocery.repositories import (
    SubCategoryRepository,
    CategoryRepository,
    ProductRepository,
)


class SubCategoryGetProductsBySlugUseCase(BaseUseCase):
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
        limit: int,
        offset: int
    ) -> ProductManyResponse:        
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

        total = await self.product_repo.get_count_records_by_subcategory_id(
            subcategory_id=subcategory.id
        )
        products = await self.product_repo.get_all_by_subcategory_id(
            subcategory_id=subcategory.id,
            limit=limit,
            offset=offset
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
