from uuid import UUID

from grocery.dto.base_dto import BaseModelDto


class SubCategoryDto(BaseModelDto):
    id: UUID
    category_id: UUID
    title: str
    slug: str
    image_id: UUID
