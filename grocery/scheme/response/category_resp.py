from uuid import UUID

from pydantic import BaseModel

from grocery.scheme.response.subcategory_resp import SubCategoryResponse


class CategoryResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    images: list[str]
    subcategories: list[SubCategoryResponse]


class CategoryManyResponse(BaseModel):
    limit: int
    offset: int
    total: int
    categories: list[CategoryResponse]
