from uuid import UUID

from fastapi import HTTPException

from grocery.scheme.request import CategoryPartialUpdateRequest
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import (
    SubCategoryResponse,
    CategoryResponse,
)
from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)
from grocery.utils import (
    ImageUrlsTool,
    Slug,
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

        if data.slug:
            Slug.validate(data.slug)
        
        if data.image_id:
            image = await self.image_repo.get_by_id(id=data.image_id)
            if not image:
                raise HTTPException(
                status_code=404,
                detail="Image not found"
            )

        category = await self.category_repo.update_partial(category_id, data)

        return CategoryResponse(
            id=category.id,
            title=category.title,
            slug=category.slug,
            images=ImageUrlsTool.get(category.image_id),
            subcategories=[
                SubCategoryResponse(
                    id=subcategory.id,
                    title=subcategory.title,
                    slug=subcategory.slug,
                    images=ImageUrlsTool.get(subcategory.image_id)
                )
                for subcategory in category.subcategories
            ]
        )
