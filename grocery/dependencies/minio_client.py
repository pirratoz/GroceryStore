from typing import AsyncIterator
from abc import ABC

from miniopy_async import Minio

from grocery.config import MinIoConfig


class MinIoConnector:
    def __init__(self) -> None:
        config = MinIoConfig()
        self.client = Minio(
            endpoint=config.HOST,
            access_key=config.ACCESS_KEY,
            secret_key=config.SECRET_KEY,
            secure=False,
        )
    
    async def get_client(self) -> AsyncIterator[Minio]:
        yield self.client


class MinIoClient(ABC):
    ...
