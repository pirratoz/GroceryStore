from uuid import UUID

from sqlalchemy.orm import joinedload
import sqlalchemy as sa

from grocery.repositories.base_repo import BaseRepository
from grocery.models import (
    SubCategory,
    Product,
)
from grocery.dto import (
    ProductWithCategoryDto,
    ProductDto,
)


class ProductRepository(BaseRepository):
    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[ProductWithCategoryDto]:
        stmt = (
            sa
            .select(Product)
            .options(
                joinedload(Product.subcategory).joinedload(SubCategory.category)
            )
            .offset(offset=offset)
            .limit(limit=limit)
            .order_by(Product.id.desc())
        )
        products = (await self.session.execute(stmt)).scalars().all()
        return ProductWithCategoryDto.many_from_orm(products)

    async def get_count_records_by_subcategory_id(
        self,
        subcategory_id: UUID
    ) -> list[ProductDto]:
        stmt = (
            sa
            .select(sa.func.count())
            .where(Product.subcategory_id == subcategory_id)
            .select_from(Product)
        )
        total = (await self.session.execute(stmt)).scalar_one()
        return total

    async def get_all_by_subcategory_id(
        self,
        subcategory_id: UUID,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[ProductWithCategoryDto]:
        stmt = (
            sa
            .select(Product)
            .where(Product.subcategory_id == subcategory_id)
            .options(
                joinedload(Product.subcategory).joinedload(SubCategory.category)
            )
            .offset(offset=offset)
            .limit(limit=limit)
            .order_by(Product.id.desc())
        )
        products = (await self.session.execute(stmt)).scalars().all()
        return ProductWithCategoryDto.many_from_orm(products)

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
            .options(
                joinedload(Product.subcategory).joinedload(SubCategory.category)
            )
        )
        product = (await self.session.execute(stmt)).scalar_one_or_none()
        return ProductWithCategoryDto.one_from_orm(product)

    async def get_one_by_slug(self, slug: str) -> ProductWithCategoryDto | None:
        stmt = (
            sa
            .select(Product)
            .where(Product.slug == slug)
            .options(
                joinedload(Product.subcategory).joinedload(SubCategory.category)
            )
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
