from uuid import UUID

from pydantic import BaseModel


class CartProductDto(BaseModel):
    id: UUID
    title: str
    price: int
    weight: int
    count: int
    image_id: UUID
    total_weight: int
    total_price: int


class CartClientDto(BaseModel):
    user_id: UUID
    products: list[CartProductDto]
    total_price: int
    total_weight: int
