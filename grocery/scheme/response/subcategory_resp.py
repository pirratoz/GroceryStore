from uuid import UUID

from pydantic import BaseModel


class SubCategoryResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    images: list[str]


class SubCategoryManyResponse(BaseModel):
    limit: int
    offset: int
    total: int
    subcategories: list[SubCategoryResponse]
