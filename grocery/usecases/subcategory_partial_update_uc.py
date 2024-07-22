from uuid import UUID

from fastapi import HTTPException

from grocery.scheme.request import SubCategoryPartialUpdateRequest
from grocery.scheme.response import SubCategoryResponse
from grocery.usecases.base_uc import BaseUseCase
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
        
        category = await self.subcategory_repo.get_one_by_id(subcategory_id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="SubCategory not found"
            )
        
        if data.image_id:
            image = await self.image_repo.get_one_by_id(data.image_id)
            if not image:
                raise HTTPException(
                    status_code=404,
                    detail="Image not found"
                )

        subcategory = await self.subcategory_repo.update_partial(
            id=subcategory_id,
            kwargs=data.model_dump(exclude_none=True)
        )

        return SubCategoryResponse.get_model(subcategory)
