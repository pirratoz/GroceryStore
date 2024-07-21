from uuid import UUID
from typing import (
    AsyncIterator,
    Literal,
)

from miniopy_async.error import S3Error
from fastapi import HTTPException
from miniopy_async import Minio
from aiohttp import (
    ClientSession,
    ClientResponse,
)

from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import ImageRepository
from grocery.config import MinIoConfig


class ImageStreamUseCase(BaseUseCase):
    def __init__(self, image_repo: ImageRepository) -> None:
        self.image_repo = image_repo
    
    @staticmethod
    async def image_download(
        size: Literal["lg", "md", "sm"],
        filename: str,
        clientS3: Minio
    ) -> ClientResponse:
        config = MinIoConfig()
        async with ClientSession() as session:
            try:
                response = await clientS3.get_object(
                    bucket_name=config.BUCKET,
                    object_name=f"{size}/{filename}",
                    session=session
                )
            except S3Error:
                raise HTTPException(
                    status_code=404,
                    detail="Image not found"
                )
            return response

    @staticmethod
    async def get_iterator(response: ClientResponse) -> AsyncIterator[bytes]:
        MB = 1024 * 1024
        async for data in response.content.iter_chunked(MB):
            yield data
        response.close()

    async def execute(
        self,
        size: Literal["lg", "md", "sm"],
        image_id: UUID,
        clientS3: Minio
    ) -> AsyncIterator[bytes]:        
        image = await self.image_repo.get_by_id(id=image_id)
        if not image:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )
        
        response = await self.image_download(size, image.filename, clientS3)
        
        return self.get_iterator(response)

