from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)


class ProductResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    images: list[str]
    price: int = Field(description="10000 ~ 100 Rub")
    weight_gramm: int = Field(description="10000 ~ 10 Kg")
    category: str
    subcategory: str


class ProductManyResponse(BaseModel):
    limit: int
    offset: int
    total: int
    products: list[ProductResponse]
