from uuid import UUID

from sqlalchemy.orm import joinedload
import sqlalchemy as sa

from grocery.repositories.base_repo import BaseRepository
from grocery.models import Category
from grocery.dto import (
    CategoryWithSubCategoryDto,
    CategoryDto
)


class CategoryRepository(BaseRepository):
    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[CategoryWithSubCategoryDto]:
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

    async def get_one_by_slug(self, slug: str) -> CategoryWithSubCategoryDto | None:
        stmt = (
            sa
            .select(Category)
            .options(joinedload(Category.subcategories))
            .where(Category.slug == slug)
        )
        category = (await self.session.execute(stmt)).unique().scalar_one_or_none()
        return CategoryWithSubCategoryDto.one_from_orm(category)

    async def get_count_records(self) -> int:
        stmt = (
            sa
            .select(sa.func.count())
            .select_from(Category)
        )
        total = (await self.session.execute(stmt)).scalar_one()
        return total
    
    async def get_one_by_id(self, id: UUID) -> CategoryWithSubCategoryDto | None:
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

    async def update_partial(
        self,
        *,
        id: UUID,
        **kwargs
    ) -> CategoryWithSubCategoryDto:
        stmt = (
            sa
            .update(Category)
            .where(Category.id == id)
            .values(kwargs)
        )
        await self.session.execute(stmt)
        return await self.get_one_by_id(id)

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
