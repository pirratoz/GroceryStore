from uuid import UUID

from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    title: str
    slug: str
    image_id: UUID
