from uuid import UUID

from fastapi import HTTPException

from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.request import SubCategoryPartialUpdateRequest
from grocery.scheme.response import SubCategoryResponse
from grocery.utils import (
    Slug,
    Images,
)
from grocery.repositories import (
    SubCategoryRepository,
    ImageRepository,
)


class SubCategoryPartialUpdateUseCase(BaseUseCase):
    def __init__(
        self,
        subcategory_repo: SubCategoryRepository,
        image_repo: ImageRepository
    ) -> None:
        self.subcategory_repo = subcategory_repo
        self.image_repo = image_repo

    async def execute(
        self,
        subcategory_id: UUID,
        data: SubCategoryPartialUpdateRequest
    ) -> SubCategoryResponse:
        
        category = await self.subcategory_repo.get_subcategory_by_id(subcategory_id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="SubCategory not found"
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

        subcategory = await self.subcategory_repo.update_partial(subcategory_id, data)

        return SubCategoryResponse(
            id=subcategory.id,
            title=subcategory.title,
            slug=subcategory.slug,
            images=Images.get(subcategory.image_id)
        )
