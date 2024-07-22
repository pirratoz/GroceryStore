from fastapi import HTTPException

from grocery.scheme.request import CategoryCreateRequest
from grocery.scheme.response import CategoryResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)


class CategoryCreateUseCase(BaseUseCase):
    def __init__(
        self,
        category_repo: CategoryRepository,
        image_repo: ImageRepository
    ) -> None:
        self.category_repo = category_repo
        self.image_repo = image_repo

    async def execute(self, category_data: CategoryCreateRequest) -> CategoryResponse:        
        category = await self.category_repo.get_one_by_slug(category_data.slug)
        if category:
            raise HTTPException(
                status_code=409,
                detail="Slug already exists"
            )
        
        image = await self.image_repo.get_one_by_id(category_data.image_id)
        if not image:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )

        category = await self.category_repo.create(
            title=category_data.title,
            slug=category_data.slug,
            image_id=category_data.image_id
        )

        return CategoryResponse.get_model_without_subcategories(category)

