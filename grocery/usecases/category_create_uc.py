from fastapi import HTTPException

from grocery.scheme.request import CategoryCreateRequest
from grocery.scheme.response import CategoryResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)
from grocery.utils import (
    Slug,
    Images,
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
        Slug.validate(category_data.slug)

        category = await self.category_repo.get_category_by_slug(category_data.slug)
        if category:
            raise HTTPException(
                status_code=409,
                detail="Slug is not unique"
            )
        
        image = await self.image_repo.get_by_id(id=category_data.image_id)
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

        return CategoryResponse(
            id=category.id,
            title=category.title,
            slug=category.slug,
            images=Images.get(category.image_id),
            subcategories=[]
        )
