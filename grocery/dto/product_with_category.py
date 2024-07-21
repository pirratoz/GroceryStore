from uuid import UUID

from grocery.dto.base_dto import BaseModelDto
from grocery.dto import (
    CategoryDto,
    SubCategoryDto,
)


class ProductWithCategoryDto(BaseModelDto):
    id: UUID
    subcategory_id: UUID
    title: str
    slug: str
    image_id: UUID
    price: int
    weight_gramm: int
    
    category: CategoryDto
    subcategory: SubCategoryDto
