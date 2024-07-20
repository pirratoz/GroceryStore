from typing import AsyncIterator

from miniopy_async import Minio
from aiohttp import ClientSession

from grocery.usecases.base_uc import BaseUseCase
from grocery.config import MinIoConfig


class ImageStreamUseCase(BaseUseCase):
    def __init__(self) -> None:
        ...

    async def execute(self, path_file: str, clientS3: Minio) -> AsyncIterator[bytes]:
        MB = 1024 * 1024
        config = MinIoConfig()
        async with ClientSession() as session:
            response = await clientS3.get_object(config.BUCKET, path_file, session)
            async for data in response.content.iter_chunked(MB):
                yield data
            response.close()
