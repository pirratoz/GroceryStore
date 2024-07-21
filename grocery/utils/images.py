from uuid import UUID

from imageworker.worker import get_available_sizes


class ImageUrlsTool:
    @staticmethod
    def get(image_id: UUID) -> list[str]:
        return [
            f"api/images/{size.path}/{image_id}"
            for size in get_available_sizes()
        ]
