# This code must be moved to a separate repository and microservice
# then the requirement to run it in a separate process will disappear.
import io

from PIL import Image
from PIL.ImageFile import ImageFile

from imageworker.photo import PhotoObject
from imageworker.size import (
    SizeImageS3,
    Size,
)


def get_ratio(size: Size, max_size: Size) -> float:
    return min(
        max_size.width / size.width,
        max_size.height / size.height
    )


def get_new_size(size: Size, ratio: float) -> Size:
    return Size(
        width=int(size.width * ratio),
        height=int(size.height * ratio)
    )


def resize(image: ImageFile, need_size: SizeImageS3) -> PhotoObject:
    buffer = io.BytesIO()

    size = Size(image.width, image.height)
    ratio = get_ratio(
        size=size,
        max_size=need_size.get_size()
    )
    new_size = get_new_size(
        size=size,
        ratio=ratio
    )

    new_image = image.resize(new_size.get_tuple(), Image.LANCZOS)
    new_image.save(buffer, image.format)

    buffer_size = buffer.tell()
    buffer.seek(0)

    photo = PhotoObject(
        content=buffer.read(),
        size=buffer_size,
        path=need_size.path
    )

    buffer.close()

    return photo


def get_available_sizes() -> tuple[SizeImageS3, ...]:
    return (
        SizeImageS3(500, 500, "lg"),
        SizeImageS3(250, 250, "md"),
        SizeImageS3(100, 100, "sm"),
    )


def handle_photo(file_bytes: bytes) -> list[PhotoObject]:
    images: list[PhotoObject] = []
    buffer = io.BytesIO(file_bytes)
    with Image.open(buffer) as image:
        for size in get_available_sizes():
            images.append(resize(image, size))
    buffer.close()
    return images
