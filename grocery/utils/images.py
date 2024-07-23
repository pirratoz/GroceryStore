from uuid import UUID

from imageworker.worker import get_available_sizes
from grocery.config import MinIoConfig
from grocery.dependencies import MinIoClient


class ImageUrlsTool:
    @staticmethod
    def get(image_id: UUID) -> list[str]:
        return [
            f"api/images/{size.path}/{image_id}"
            for size in get_available_sizes()
        ]

    @staticmethod
    async def delete(clientS3: MinIoClient, filename: str) -> bool:
        config = MinIoConfig()
        await clientS3.remove_objects(
            config.BUCKET,
            delete_object_list=[
                f"{size.path}/{filename}"
                for size in get_available_sizes()
            ]
        )
