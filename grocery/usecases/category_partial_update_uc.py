from uuid import UUID

from fastapi import HTTPException

from grocery.scheme.request import CategoryPartialUpdateRequest
from grocery.scheme.response import CategoryResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)


class CategoryPartialUpdateUseCase(BaseUseCase):
    def __init__(
        self,
        category_repo: CategoryRepository,
        image_repo: ImageRepository
    ) -> None:
        self.category_repo = category_repo
        self.image_repo = image_repo

    async def execute(
        self,
        category_id: UUID,
        data: CategoryPartialUpdateRequest
    ) -> CategoryResponse:
        
        category = await self.category_repo.get_category_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )
        
        if data.image_id:
            image = await self.image_repo.get_by_id(id=data.image_id)
            if not image:
                raise HTTPException(
                status_code=404,
                detail="Image not found"
            )

        category = await self.category_repo.update_partial(category_id, data)

        return CategoryResponse.get_model_with_subcategories(category)
