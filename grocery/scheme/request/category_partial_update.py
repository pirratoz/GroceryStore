from uuid import UUID
from re import match

from fastapi import HTTPException

from pydantic import (
    BaseModel,
    field_validator,
)


class CategoryPartialUpdateRequest(BaseModel):
    title: str | None = None
    slug: str | None = None
    image_id: UUID | None = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str | None) -> str | None:
        if value and not match(r"^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$", value):
            raise HTTPException(
                status_code=422,
                detail="This not slug"
            )
        return value
