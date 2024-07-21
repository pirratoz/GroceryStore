from uuid import UUID

from fastapi import HTTPException

from grocery.scheme.response import SubCategoryResponse
from grocery.repositories import SubCategoryRepository
from grocery.usecases.base_uc import BaseUseCase
from grocery.utils import ImageUrlsTool


class SubCategoryDeleteUseCase(BaseUseCase):
    def __init__(self, subcategory_repo: SubCategoryRepository) -> None:
        self.subcategory_repo = subcategory_repo

    async def execute(self, id: UUID) -> SubCategoryResponse:
        subcategory = await self.subcategory_repo.get_subcategory_by_id(id)

        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail="SubCategory not found"
            )

        await self.subcategory_repo.delete_by_id(id)
        return SubCategoryResponse(
            id=subcategory.id,
            title=subcategory.title,
            slug=subcategory.slug,
            images=ImageUrlsTool.get(subcategory.image_id)
        )
