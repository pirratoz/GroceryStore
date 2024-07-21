from uuid import UUID

import sqlalchemy as sa

from grocery.repositories.base_repo import BaseRepository
from grocery.models import SubCategory
from grocery.dto import SubCategoryDto


class SubCategoryRepository(BaseRepository):
    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[SubCategoryDto]:
        stmt = (
            sa
            .select(SubCategory)
            .offset(offset=offset)
            .limit(limit=limit)
            .order_by(SubCategory.id.desc())
        )
        categories = (await self.session.execute(stmt)).scalars().all()
        return SubCategoryDto.many_from_orm(categories)

    async def get_one_by_slug(self, slug: str) -> SubCategoryDto | None:
        stmt = (
            sa
            .select(SubCategory)
            .where(SubCategory.slug == slug)
        )
        category = (await self.session.execute(stmt)).scalar_one_or_none()
        return SubCategoryDto.one_from_orm(category)

    async def get_count_records(self) -> int:
        stmt = (
            sa
            .select(sa.func.count())
            .select_from(SubCategory)
        )
        total = (await self.session.execute(stmt)).scalar_one()
        return total
    
    async def get_one_by_id(self, id: UUID) -> SubCategoryDto | None:
        stmt = (
            sa
            .select(SubCategory)
            .where(SubCategory.id == id)
        )
        category = (await self.session.execute(stmt)).scalar_one_or_none()
        return SubCategoryDto.one_from_orm(category)

    async def delete_by_id(self, id: UUID) -> None:
        stmt = (
            sa
            .delete(SubCategory)
            .where(SubCategory.id == id)
        )
        await self.session.execute(stmt)

    async def update_partial(
        self,
        *,
        id: UUID,
        **kwargs
    ) -> SubCategoryDto:
        stmt = (
            sa
            .update(SubCategory)
            .where(SubCategory.id == id)
            .values(kwargs)
        )
        await self.session.execute(stmt)
        return await self.get_one_by_id(id)

    async def create(
        self,
        *,
        category_id: UUID,
        title: str,
        slug: str,
        image_id: UUID,
    ) -> SubCategoryDto:
        category = SubCategory(
            category_id=str(category_id),
            title=title,
            slug=slug,
            image_id=str(image_id)
        )
        self.session.add(category)
        await self.session.flush()
        return SubCategoryDto.one_from_orm(category)
    