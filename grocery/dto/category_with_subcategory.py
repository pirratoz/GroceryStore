from uuid import UUID

from grocery.dto.base_dto import BaseModelDto
from grocery.dto.subcategory import SubCategoryDto


class CategoryWithSubCategoryDto(BaseModelDto):
    id: UUID
    title: str
    slug: str
    image_id: UUID
    subcategories: list[SubCategoryDto]
