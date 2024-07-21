from uuid import UUID

from pydantic import BaseModel

from grocery.scheme.response.subcategory_resp import SubCategoryResponse
from grocery.utils import ImageUrlsTool
from grocery.dto import (
    CategoryWithSubCategoryDto,
    CategoryDto,
)


class CategoryResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    images: list[str]
    subcategories: list[SubCategoryResponse]
    
    @staticmethod
    def get_model_with_subcategories(
        category: CategoryWithSubCategoryDto
    ) -> "CategoryResponse":
        return CategoryResponse(
            id=category.id,
            title=category.title,
            slug=category.slug,
            images=ImageUrlsTool.get(category.image_id),
            subcategories=[
                SubCategoryResponse.get_model(subcategory)
                for subcategory in category.subcategories
            ]
        )

    @staticmethod
    def get_model_without_subcategories(
        category: CategoryDto | CategoryWithSubCategoryDto
    ) -> "CategoryResponse":
        return CategoryResponse(
            id=category.id,
            title=category.title,
            slug=category.slug,
            images=ImageUrlsTool.get(category.image_id),
            subcategories=[]
        )


class CategoryManyResponse(BaseModel):
    limit: int
    offset: int
    total: int
    categories: list[CategoryResponse]
