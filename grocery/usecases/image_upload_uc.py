from concurrent.futures import ProcessPoolExecutor
import asyncio
from uuid import uuid4
import io

from miniopy_async import Minio
from fastapi import UploadFile

from grocery.usecases.base_uc import BaseUseCase
from grocery.repositories import ImageRepository
from grocery.scheme.response import ImageResponse
from grocery.scheme.response import CategoryResponse
from grocery.config import MinIoConfig
from imageworker.worker import handle_photo


class ImageUploadUseCase(BaseUseCase):
    def __init__(self, image_repo: ImageRepository) -> None:
        self.image_repo = image_repo

    async def execute(self, file: UploadFile, clientS3: Minio) -> CategoryResponse:
        image_id = uuid4()
        file_ext = file.filename.split(".")[-1]
        filename = f"{image_id}.{file_ext}"

        config = MinIoConfig()
        loop = asyncio.get_running_loop()
        with ProcessPoolExecutor() as pool:
            files = await loop.run_in_executor(
                pool, handle_photo, await file.read()
            )
            for photo in files:
                buffer = io.BytesIO(photo.content)
                await clientS3.put_object(
                    bucket_name=config.BUCKET,
                    object_name=f"{photo.path}/{filename}",
                    data=buffer,
                    length=photo.size
                )
                buffer.close()

        image = await self.image_repo.create(filename=filename)

        return ImageResponse(id=image.id, filename=image.filename)
