from grocery.repositories import SubCategoryRepository
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import (
    SubCategoryManyResponse,
    SubCategoryResponse,
)
from grocery.utils import ImageUrlsTool


class SubCategoryGetAllUseCase(BaseUseCase):
    def __init__(self, subcategory_repo: SubCategoryRepository) -> None:
        self.subcategory_repo = subcategory_repo

    async def execute(self, limit: int, offset: int) -> SubCategoryManyResponse:
        total = await self.subcategory_repo.get_count_record()
        subcategories = await self.subcategory_repo.get_subcategories_by_offset(
            limit=limit,
            offset=offset,
        )
        return SubCategoryManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            subcategories=[
                SubCategoryResponse(
                    id=category.id,
                    title=category.title,
                    slug=category.slug,
                    images=ImageUrlsTool.get(category.image_id)
                )
                for category in subcategories
            ]
        )

