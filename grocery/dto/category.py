from uuid import UUID

from grocery.dto.base_dto import BaseModelDto


class CategoryDto(BaseModelDto):
    id: UUID
    title: str
    slug: str
    image_id: UUID
