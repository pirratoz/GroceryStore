from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from grocery.dto import ProductWithCategoryDto
from grocery.utils import ImageUrlsTool


class ProductResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    images: list[str]
    price: int = Field(description="10000 ~ 100 Rub")
    weight_gramm: int = Field(description="10000 ~ 10 Kg")
    category_title: str
    subcategory_title: str

    @staticmethod
    def get_model(product: ProductWithCategoryDto) -> "ProductResponse":
        return ProductResponse(
            id=product.id,
            title=product.title,
            slug=product.slug,
            images=ImageUrlsTool.get(product.image_id),
            price=product.price,
            weight_gramm=product.weight_gramm,
            category_title=product.subcategory.category.title,
            subcategory_title=product.subcategory.title
        )


class ProductManyResponse(BaseModel):
    limit: int
    offset: int
    total: int
    products: list[ProductResponse]
