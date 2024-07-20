from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories.category_repo import CategoryRepository
from grocery.scheme.response import (
    CategoryManyResponse,
    CategoryResponse,
)
from imageworker.worker import get_available_sizes


class CategoryGetAllUseCase(BaseUseCase):
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self, limit: int, offset: int) -> CategoryManyResponse:
        total = await self.category_repo.get_count_record()
        categories = await self.category_repo.get_categories_by_offset(
            limit=limit,
            offset=offset,
        )
        return CategoryManyResponse(
            limit=limit,
            offset=offset,
            total=total,
            categories=[
                CategoryResponse(
                    id=category.id,
                    title=category.title,
                    slug=category.slug,
                    images=[
                        f"api/images/{size.path}/{category.image_id}"
                        for size in get_available_sizes()
                    ],
                    subcategories=[
                        
                    ]
                )
                for category in categories
            ],
        )

