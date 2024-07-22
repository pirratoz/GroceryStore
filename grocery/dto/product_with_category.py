from uuid import UUID

from grocery.dto.subcategory_with_category import SubCategoryWithCategoryDto
from grocery.dto.base_dto import BaseModelDto


class ProductWithCategoryDto(BaseModelDto):
    id: UUID
    subcategory_id: UUID
    title: str
    slug: str
    image_id: UUID
    price: int
    weight_gramm: int
    
    subcategory: SubCategoryWithCategoryDto
