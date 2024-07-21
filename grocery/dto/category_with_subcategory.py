from uuid import UUID

from grocery.dto.subcategory import SubCategoryDto
from grocery.dto.base_dto import BaseModelDto


class CategoryWithSubCategoryDto(BaseModelDto):
    id: UUID
    title: str
    slug: str
    image_id: UUID
    subcategories: list[SubCategoryDto]
