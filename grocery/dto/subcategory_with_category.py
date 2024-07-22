from uuid import UUID

from grocery.dto.base_dto import BaseModelDto
from grocery.dto.category import CategoryDto


class SubCategoryWithCategoryDto(BaseModelDto):
    id: UUID
    category_id: UUID
    title: str
    slug: str
    image_id: UUID
    category: CategoryDto
