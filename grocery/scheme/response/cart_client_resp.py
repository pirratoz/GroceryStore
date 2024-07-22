from uuid import UUID

from pydantic import BaseModel

from grocery.utils import ImageUrlsTool
from grocery.dto import (
    CartProductDto,
    CartClientDto,
)


class CartProductResponse(BaseModel):
    id: UUID
    title: str
    price: int
    weight: int
    count: int
    images: list[str]
    total_weight: int
    total_price: int

    @staticmethod
    def get_model(product: CartProductDto) -> "CartProductResponse":
        return CartProductResponse(
            id=product.id,
            title=product.title,
            price=product.price,
            weight=product.weight,
            count=product.count,
            images=ImageUrlsTool.get(product.image_id),
            total_weight=product.total_weight,
            total_price=product.total_price
        )


class CartClientResponse(BaseModel):
    user_id: UUID
    products: list[CartProductResponse] = []
    total_price: int = 0
    total_weight: int = 0

    @staticmethod
    def get_model(cart: CartClientDto) -> "CartClientResponse":
        return CartClientResponse(
            user_id=cart.user_id,
            products=[
                CartProductResponse.get_model(product)
                for product in cart.products
            ],
            total_price=cart.total_price,
            total_weight=cart.total_weight
        )
