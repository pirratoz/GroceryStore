from uuid import UUID

from grocery.dto.base_dto import BaseModelDto


class CartDto(BaseModelDto):
    id: UUID
    user_id: UUID
    product_id: UUID
    count: int
