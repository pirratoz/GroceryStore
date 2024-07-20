from uuid import UUID

from pydantic import BaseModel


class SubCategoryPartialUpdateRequest(BaseModel):
    category_id: UUID | None = None
    title: str | None = None
    slug: str | None = None
    image_id: UUID | None = None
