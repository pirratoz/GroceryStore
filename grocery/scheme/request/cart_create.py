from uuid import UUID

from pydantic import BaseModel


class CartCreateRequest(BaseModel):
    product_id: UUID
    count: int
