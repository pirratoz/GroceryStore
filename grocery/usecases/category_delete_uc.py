from uuid import UUID

from fastapi import HTTPException

from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)
from grocery.scheme.response import CategoryResponse
from grocery.usecases.base_uc import BaseUseCase
from grocery.dependencies import MinIoClient
from grocery.utils import ImageUrlsTool


class CategoryDeleteUseCase(BaseUseCase):
    def __init__(
        self,
        category_repo: CategoryRepository,
        image_repo: ImageRepository
    ) -> None:
        self.category_repo = category_repo
        self.image_repo = image_repo

    async def execute(self, id: UUID, clientS3: MinIoClient) -> CategoryResponse:
        category = await self.category_repo.get_one_by_id(id)

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        if (image := await self.image_repo.get_one_by_id(category.image_id)):
            await self.image_repo.delete_by_id(category.image_id)
            await ImageUrlsTool.delete(clientS3, image.filename)

        await self.category_repo.delete_by_id(id)

        return CategoryResponse.get_model_with_subcategories(category)
    