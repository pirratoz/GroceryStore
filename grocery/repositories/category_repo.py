from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from grocery.repositories.base_repo import BaseRepository
from grocery.models import (
    Category,
    SubCategory,
)
from grocery.scheme.request import CategoryPartialUpdateRequest
from grocery.dto import (
    CategoryWithSubCategoryDto,
    CategoryDto
)


class CategoryRepository(BaseRepository):
    async def get_categories_by_offset(self, limit: int, offset: int) -> list[CategoryWithSubCategoryDto]:
        stmt = (
            sa
            .select(Category)
            .options(joinedload(Category.subcategories))
            .offset(offset=offset)
            .limit(limit=limit)
            .order_by(Category.id.desc())
        )
        categories = (await self.session.execute(stmt)).unique().scalars().all()
        return CategoryWithSubCategoryDto.many_from_orm(categories)

    async def get_category_by_slug(self, slug: str) -> CategoryWithSubCategoryDto | None:
        stmt = (
            sa
            .select(Category)
            .options(joinedload(Category.subcategories))
            .where(Category.slug == slug)
        )
        category = (await self.session.execute(stmt)).scalar_one_or_none()
        return CategoryWithSubCategoryDto.one_from_orm(category)

    async def get_count_record(self) -> int:
        stmt = sa.select(sa.func.count()).select_from(Category)
        total = (await self.session.execute(stmt)).scalar_one()
        return total
    
    async def get_category_by_id(self, id: UUID) -> CategoryWithSubCategoryDto | None:
        stmt = (
            sa
            .select(Category)
            .options(joinedload(Category.subcategories))
            .where(Category.id == id)
        )
        category = (await self.session.execute(stmt)).unique().scalar_one_or_none()
        return CategoryWithSubCategoryDto.one_from_orm(category)

    async def delete_by_id(self, id: UUID) -> None:
        stmt = sa.delete(Category).where(Category.id == id)
        await self.session.execute(stmt)

    async def update_partial(self, id: UUID, data: CategoryPartialUpdateRequest) -> CategoryWithSubCategoryDto:
        stmt = sa.update(Category).where(Category.id == id).values(**data.model_dump(exclude_none=True))
        await self.session.execute(stmt)
        return await self.get_category_by_id(id)

    async def create(
        self,
        *,
        title: str,
        slug: str,
        image_id: UUID,
    ) -> CategoryDto:
        category = Category(
            title=title,
            slug=slug,
            image_id=str(image_id)
        )
        self.session.add(category)
        await self.session.flush()
        return CategoryDto.one_from_orm(category)
    
