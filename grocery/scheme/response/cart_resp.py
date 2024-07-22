from uuid import UUID

from pydantic import BaseModel


class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    count: int
