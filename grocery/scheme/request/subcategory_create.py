from uuid import UUID

from pydantic import BaseModel


class SubCategoryCreateRequest(BaseModel):
    category_id: UUID
    title: str
    slug: str
    image_id: UUID
