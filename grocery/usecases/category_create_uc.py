from fastapi import HTTPException

from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.request import CategoryCreateRequest
from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)
from grocery.scheme.response import CategoryResponse
from grocery.utils import Slug
from imageworker.worker import get_available_sizes

class CategoryCreateUseCase(BaseUseCase):
    def __init__(
        self,
        category_repo: CategoryRepository,
        image_repo: ImageRepository
    ) -> None:
        self.category_repo = category_repo
        self.image_repo = image_repo

    async def execute(self, category_data: CategoryCreateRequest) -> CategoryResponse:        
        Slug.validate(category_data.slug)

        category = await self.category_repo.get_category_by_slug(category_data.slug)
        if category:
            raise HTTPException(
                status_code=409,
                detail="Slug is not unique"
            )
        
        category = await self.category_repo.create(
            title=category_data.title,
            slug=category_data.slug,
            image_id=category_data.image_id
        )
        image = await self.image_repo.get_by_id(id=category_data.image_id)

        return CategoryResponse(
            id=category.id,
            title=category.title,
            slug=category.slug,
            images=[
                f"api/images/{size.path}/{image.id}"
                for size in get_available_sizes()
            ],
            subcategories=[]
        )
