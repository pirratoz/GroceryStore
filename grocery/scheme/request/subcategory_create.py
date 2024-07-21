from uuid import UUID
from re import match

from fastapi import HTTPException

from pydantic import (
    BaseModel,
    field_validator,
)


class SubCategoryCreateRequest(BaseModel):
    category_id: UUID
    title: str
    slug: str
    image_id: UUID

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str) -> str:
        if not match(r"^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$", value):
            raise HTTPException(
                status_code=422,
                detail="This not slug"
            )
        return value
