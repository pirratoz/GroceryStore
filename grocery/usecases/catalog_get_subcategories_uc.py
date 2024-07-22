from fastapi import HTTPException

from grocery.scheme.response import (
    SubCategoryManyResponse,
    SubCategoryResponse,
)
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import (
    SubCategoryRepository,
    CategoryRepository,
)


class CatalogGetSubcategoriesUseCase(BaseUseCase):
    def __init__(
        self,
        category_repo: CategoryRepository,
        subcategory_repo: SubCategoryRepository
    ) -> None:
        self.category_repo = category_repo
        self.subcategory_repo = subcategory_repo

    async def execute(
        self,
        slug_category: str,
        limit: int,
        offset: int
    ) -> SubCategoryManyResponse:        
        category = await self.category_repo.get_one_by_slug(slug_category)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        total = await self.subcategory_repo.get_count_records_by_category_id(
            category_id=category.id
        )
        subcategories = await self.subcategory_repo.get_all_by_category_id(
            category_id=category.id,
            limit=limit,
            offset=offset,
        )

        return SubCategoryManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            subcategories=[
                SubCategoryResponse.get_model(subcategory)
                for subcategory in subcategories
            ]
        )
