from grocery.repositories import CategoryRepository
from grocery.usecases.base_uc import BaseUseCase
from grocery.scheme.response import (
    CategoryManyResponse,
    CategoryResponse,
)


class CategoryGetAllUseCase(BaseUseCase):
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> CategoryManyResponse:
        total = await self.category_repo.get_count_records()
        categories = await self.category_repo.get_all(
            limit=limit,
            offset=offset,
        )

        return CategoryManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            categories=[
                CategoryResponse.get_model_with_subcategories(category)
                for category in categories
            ]
        )
