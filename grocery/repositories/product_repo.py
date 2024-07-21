from uuid import UUID

import sqlalchemy as sa

from grocery.repositories.base_repo import BaseRepository
from grocery.models import Product
from grocery.dto import (
    ProductWithCategoryDto,
    ProductDto,
)


class ProductRepository(BaseRepository):
    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[ProductDto]:
        stmt = (
            sa
            .select(Product)
            .offset(offset=offset)
            .limit(limit=limit)
            .order_by(Product.id.desc())
        )
        products = (await self.session.execute(stmt)).scalars().all()
        return ProductDto.many_from_orm(products)

    async def get_count_records(self) -> int:
        stmt = (
            sa
            .select(sa.func.count())
            .select_from(Product)
        )
        total = (await self.session.execute(stmt)).scalar_one()
        return total
    
    async def get_one_by_id(self, id: UUID) -> ProductWithCategoryDto | None:
        stmt = (
            sa
            .select(Product)
            .where(Product.id == id)
        )
        product = (await self.session.execute(stmt)).scalar_one_or_none()
        return ProductWithCategoryDto.one_from_orm(product)

    async def get_one_by_slug(self, slug: str) -> ProductWithCategoryDto | None:
        stmt = (
            sa
            .select(Product)
            .where(Product.slug == slug)
        )
        product = (await self.session.execute(stmt)).scalar_one_or_none()
        return ProductWithCategoryDto.one_from_orm(product)

    async def delete_by_id(self, id: UUID) -> None:
        stmt = sa.delete(Product).where(Product.id == id)
        await self.session.execute(stmt)

    async def update_partial(
        self,
        *,
        id: UUID,
        **kwargs
    ) -> ProductWithCategoryDto:
        stmt = (
            sa
            .update(Product)
            .where(Product.id == id)
            .values(kwargs)
        )
        await self.session.execute(stmt)
        return await self.get_one_by_id(id)

    async def create(
        self,
        *,
        subcategory_id: UUID,
        title: str,
        slug: str,
        image_id: UUID,
        price: int,
        weight_gramm: int
    ) -> ProductDto:
        product = Product(
            subcategory_id=subcategory_id,
            title=title,
            slug=slug,
            image_id=image_id,
            price=price,
            weight_gramm=weight_gramm
        )
        self.session.add(product)
        await self.session.flush()
        return ProductDto.one_from_orm(product)
