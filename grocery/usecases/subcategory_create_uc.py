from fastapi import HTTPException

from grocery.scheme.request import SubCategoryCreateRequest
from grocery.scheme.response import SubCategoryResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import (
    SubCategoryRepository,
    ImageRepository,
)
from grocery.utils import Slug


class SubCategoryCreateUseCase(BaseUseCase):
    def __init__(
        self,
        subcategory_repo: SubCategoryRepository,
        image_repo: ImageRepository
    ) -> None:
        self.subcategory_repo = subcategory_repo
        self.image_repo = image_repo

    async def execute(self, data: SubCategoryCreateRequest) -> SubCategoryResponse:        
        Slug.validate(data.slug)

        subcategory = await self.subcategory_repo.get_subcategory_by_slug(data.slug)
        if subcategory:
            raise HTTPException(
                status_code=409,
                detail="Slug is not unique"
            )
        
        image = await self.image_repo.get_by_id(id=data.image_id)
        if not image:
            raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

        subcategory = await self.subcategory_repo.create(
            category_id=data.category_id,
            title=data.title,
            slug=data.slug,
            image_id=data.image_id
        )

        return SubCategoryResponse.get_model(subcategory)
