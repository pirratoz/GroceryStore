from uuid import UUID

import sqlalchemy as sa

from grocery.repositories.base_repo import BaseRepository
from grocery.models import Image
from grocery.dto import ImageDto


class ImageRepository(BaseRepository):    
    async def get_one_by_id(self, id: UUID) -> ImageDto | None:
        stmt = (
            sa
            .select(Image)
            .where(Image.id == id)
        )
        image = (await self.session.execute(stmt)).scalar_one_or_none()
        return ImageDto.one_from_orm(image)

    async def create(self, *, filename: str) -> ImageDto:
        image = Image(filename=filename)
        self.session.add(image)
        await self.session.flush()
        return ImageDto.one_from_orm(image)
