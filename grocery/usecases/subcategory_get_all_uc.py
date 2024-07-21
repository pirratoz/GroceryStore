from grocery.repositories import SubCategoryRepository
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import (
    SubCategoryManyResponse,
    SubCategoryResponse,
)


class SubCategoryGetAllUseCase(BaseUseCase):
    def __init__(self, subcategory_repo: SubCategoryRepository) -> None:
        self.subcategory_repo = subcategory_repo

    async def execute(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> SubCategoryManyResponse:
        total = await self.subcategory_repo.get_count_records()
        subcategories = await self.subcategory_repo.get_all(
            limit=limit,
            offset=offset,
        )

        return SubCategoryManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            subcategories=[
                SubCategoryResponse.get_model(subcategory)
                for subcategory in subcategories
            ]
        )

