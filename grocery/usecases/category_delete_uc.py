from uuid import UUID

from fastapi import HTTPException

from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories.category_repo import CategoryRepository
from grocery.scheme.response import (
    SubCategoryResponse,
    CategoryResponse,
)
from grocery.utils import Images


class CategoryDeleteUseCase(BaseUseCase):
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self, id: UUID) -> CategoryResponse:
        category = await self.category_repo.get_category_by_id(id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        await self.category_repo.delete_by_id(id)
        return CategoryResponse(
            id=category.id,
            title=category.title,
            slug=category.slug,
            images=Images.get(category.image_id),
            subcategories=[
                SubCategoryResponse(
                    id=subcategory.id,
                    title=subcategory.title,
                    slug=subcategory.slug,
                    images=Images.get(subcategory.image_id)
                )
                for subcategory in category.subcategories
            ]
        )
    