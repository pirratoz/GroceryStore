from uuid import UUID

from pydantic import BaseModel


class CategoryPartialUpdateRequest(BaseModel):
    title: str | None = None
    slug: str | None = None
    image_id: UUID | None = None
