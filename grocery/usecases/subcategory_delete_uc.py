from uuid import UUID

from fastapi import HTTPException

from grocery.scheme.response import SubCategoryResponse
from grocery.dependencies import MinIoClient
from grocery.utils import ImageUrlsTool
from grocery.repositories import (
    SubCategoryRepository,
    ImageRepository,
)
from grocery.usecases.base_uc import BaseUseCase


class SubCategoryDeleteUseCase(BaseUseCase):
    def __init__(
        self,
        subcategory_repo: SubCategoryRepository,
        image_repo: ImageRepository
    ) -> None:
        self.subcategory_repo = subcategory_repo
        self.image_repo = image_repo

    async def execute(self, id: UUID, clientS3: MinIoClient) -> SubCategoryResponse:
        subcategory = await self.subcategory_repo.get_one_by_id(id)

        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail="SubCategory not found"
            )

        if (image := await self.image_repo.get_one_by_id(subcategory.image_id)):
            await self.image_repo.delete_by_id(subcategory.image_id)
            await ImageUrlsTool.delete(clientS3, image.filename)
        
        await self.subcategory_repo.delete_by_id(id)

        return SubCategoryResponse.get_model(subcategory)
    