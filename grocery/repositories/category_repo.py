from uuid import UUID

import sqlalchemy as sa

from grocery.repositories.base_repo import BaseRepository
from grocery.models import (
    Category,
    SubCategory,
)
from grocery.dto import CategoryDto


class CategoryRepository(BaseRepository):
    async def get_categories_by_offset(self, limit: int, offset: int) -> list[Category]:
        stmt = sa.select(Category).offset(offset=offset).limit(limit=limit).order_by(Category.id.desc())
        categories = (await self.session.execute(stmt)).scalars().all()
        return CategoryDto.many_from_orm(categories)

    async def get_category_by_slug(self, slug: str) -> Category | None:
        stmt = sa.select(Category).where(Category.slug == slug)
        category = (await self.session.execute(stmt)).scalar_one_or_none()
        return CategoryDto.one_from_orm(category)

    async def get_count_record(self) -> int:
        stmt = sa.select(sa.func.count()).select_from(Category)
        total = (await self.session.execute(stmt)).scalar_one()
        return total
    
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
    
