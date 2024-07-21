from uuid import UUID

import sqlalchemy as sa

from grocery.scheme.request import SubCategoryPartialUpdateRequest
from grocery.repositories.base_repo import BaseRepository
from grocery.models import SubCategory
from grocery.dto import SubCategoryDto


class SubCategoryRepository(BaseRepository):
    async def get_subcategories_by_offset(self, limit: int, offset: int) -> list[SubCategoryDto]:
        stmt = sa.select(SubCategory).offset(offset=offset).limit(limit=limit).order_by(SubCategory.id.desc())
        categories = (await self.session.execute(stmt)).scalars().all()
        return SubCategoryDto.many_from_orm(categories)

    async def get_subcategory_by_slug(self, slug: str) -> SubCategoryDto | None:
        stmt = sa.select(SubCategory).where(SubCategory.slug == slug)
        category = (await self.session.execute(stmt)).scalar_one_or_none()
        return SubCategoryDto.one_from_orm(category)

    async def get_count_record(self) -> int:
        stmt = sa.select(sa.func.count()).select_from(SubCategory)
        total = (await self.session.execute(stmt)).scalar_one()
        return total
    
    async def get_subcategory_by_id(self, id: UUID) -> SubCategoryDto | None:
        stmt = sa.select(SubCategory).where(SubCategory.id == id)
        category = (await self.session.execute(stmt)).scalar_one_or_none()
        return SubCategoryDto.one_from_orm(category)

    async def delete_by_id(self, id: UUID) -> None:
        stmt = sa.delete(SubCategory).where(SubCategory.id == id)
        await self.session.execute(stmt)

    async def update_partial(self, id: UUID, data: SubCategoryPartialUpdateRequest) -> SubCategoryDto:
        stmt = sa.update(SubCategory).where(SubCategory.id == id).values(**data.model_dump(exclude_none=True))
        await self.session.execute(stmt)
        return await self.get_subcategory_by_id(id)

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
    