from uuid import UUID

from fastapi import HTTPException

from grocery.repositories import CategoryRepository
from grocery.scheme.response import CategoryResponse
from grocery.usecases.base_uc import BaseUseCase


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

        return CategoryResponse.get_model_with_subcategories(category)
    