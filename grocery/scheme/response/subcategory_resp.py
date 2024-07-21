from uuid import UUID

from pydantic import BaseModel

from grocery.utils import ImageUrlsTool
from grocery.dto import SubCategoryDto


class SubCategoryResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    images: list[str]

    @staticmethod
    def get_model(subcategory: SubCategoryDto) -> "SubCategoryResponse":
        return SubCategoryResponse(
            id=subcategory.id,
            title=subcategory.title,
            slug=subcategory.slug,
            images=ImageUrlsTool.get(subcategory.image_id)
        )


class SubCategoryManyResponse(BaseModel):
    limit: int
    offset: int
    total: int
    subcategories: list[SubCategoryResponse]
