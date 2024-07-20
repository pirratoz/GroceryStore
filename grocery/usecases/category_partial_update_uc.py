from uuid import UUID

from fastapi import HTTPException

from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.request import CategoryPartialUpdateRequest
from grocery.scheme.response import CategoryResponse
from grocery.utils import Slug
from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)
from imageworker.worker import get_available_sizes


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
                status_code=409,
                detail="Category not found"
            )

        if data.slug:
            Slug.validate(data.slug)
        
        if data.image_id:
            image = await self.image_repo.get_by_id(id=data.image_id)
            if not image:
                raise HTTPException(
                status_code=409,
                detail="Image not found"
            )

        category = await self.category_repo.update_partial(category_id, data)

        return CategoryResponse(
            id=category.id,
            title=category.title,
            slug=category.slug,
            images=[
                f"api/images/{size.path}/{category.image_id}"
                for size in get_available_sizes()
            ],
            subcategories=[
                
            ]
        )
