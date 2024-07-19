from uuid import UUID

from grocery.dto.base_dto import BaseModelDto


class ImageDto(BaseModelDto):
    id: UUID
    filename: str

