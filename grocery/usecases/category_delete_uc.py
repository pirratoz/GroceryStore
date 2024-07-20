from uuid import UUID

from fastapi import HTTPException

from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories.category_repo import CategoryRepository
from grocery.dto import CategoryDto


class CategoryDeleteUseCase(BaseUseCase):
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self, id: UUID) -> CategoryDto:
        category = await self.category_repo.get_category_by_id(id)

        if not category:
            raise HTTPException(
                status_code=409,
                detail="Category not found"
            )

        await self.category_repo.delete_by_id(id)
        return category
    