from uuid import UUID

from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: UUID
    filename: str
