from uuid import UUID

import sqlalchemy as sa

from grocery.repositories.base_repo import BaseRepository
from grocery.models import (
    Product,
    Cart,
)
from grocery.dto import (
    CartDto,
    CartClientDto,
    CartProductDto,
)


class CartRepository(BaseRepository):
    async def clear_all(self, user_id: UUID) -> bool:
        stmt = (
            sa
            .delete(Cart)
            .where(Cart.user_id == user_id)
        )
        await self.session.execute(stmt)
        return True

    async def delete_by_id(self, cart_id: UUID) -> bool:
        stmt = (
            sa
            .delete(Cart)
            .where(Cart.id == cart_id)
        )
        await self.session.execute(stmt)
        return True

    async def get_one_by_id(self, cart_id: UUID) -> CartDto | None:
        stmt = (
            sa
            .select(Cart)
            .where(Cart.id == cart_id)
        )
        cart = (await self.session.execute(stmt)).scalar_one_or_none()
        return CartDto.one_from_orm(cart)

    async def check_in_cart(
        self,
        user_id: UUID,
        product_id: UUID
    ) -> CartDto | None:
        stmt = (
            sa
            .select(Cart)
            .where(
                Cart.user_id == user_id,
                Cart.product_id == product_id
            )
        )
        cart = (await self.session.execute(stmt)).scalar_one_or_none()
        return CartDto.one_from_orm(cart)

    async def update_partial(
        self,
        *,
        cart_id: UUID,
        **kwargs
    ) -> CartDto:
        stmt = (
            sa
            .update(Cart)
            .where(Cart.id == cart_id)
            .values(kwargs)
        )
        await self.session.execute(stmt)
        return await self.get_one_by_id(cart_id)

    async def get_client_cart(self, user_id: UUID) -> CartClientDto:
        stmt_total = (
            sa
            .select(
                sa.func.sum(Cart.count * Product.price).label("total_price"),
                sa.func.sum(Cart.count * Product.weight_gramm).label("total_weight"),
            )
            .where(Cart.user_id == user_id)
            .join(Product, Cart.product_id == Product.id)
        )
        stmt_info = (
            sa
            .select(
                Product.id.label("id"),
                Product.title.label("title"),
                Product.price.label("price"),
                Product.weight_gramm.label("weight"),
                Cart.count.label("count"),
                Product.image_id.label("image_id"),
                (Product.weight_gramm * Cart.count).label("total_weight"),
                (Product.price * Cart.count).label("total_price")
            )
            .where(Cart.user_id == user_id)
            .join(Product, Cart.product_id == Product.id)
        )

        result_total = (await self.session.execute(stmt_total)).fetchone()
        products = (await self.session.execute(stmt_info)).fetchall()

        return CartClientDto(
            user_id=user_id,
            products=[
                CartProductDto(
                    id=product.id,
                    title=product.title,
                    price=product.price,
                    weight=product.weight,
                    count=product.count,
                    image_id=product.image_id,
                    total_price=product.total_price,
                    total_weight=product.total_weight
                )
                for product in products
            ],
            total_price=result_total.total_price,
            total_weight=result_total.total_weight
        )

    async def create(
        self,
        *,
        user_id: UUID,
        product_id: UUID,
        count: int
    ) -> CartDto:
        cart = Cart(
            user_id=user_id,
            product_id=product_id,
            count=count
        )
        self.session.add(cart)
        await self.session.flush()
        return CartDto.one_from_orm(cart)
