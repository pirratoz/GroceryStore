from typing import (
    Literal,
    AsyncIterable,
)

from fastapi.responses import StreamingResponse
from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
)

from grocery.dependencies import (
    Session,
    IsAdmin,
    MinIoClient,
)
from grocery.repositories import ImageRepository
from grocery.usecases import (
    ImageUploadUseCase,
    ImageStreamUseCase,
)
from grocery.scheme.response import ImageResponse


images = APIRouter()


@images.get("/{size}/{id}")
async def download_image(
    size: Literal["lg", "md", "sm"],
    id: str,
    clientS3: MinIoClient = Depends()
) -> StreamingResponse:
    content = ImageStreamUseCase().execute(f"{size}/{id}", clientS3)
    return StreamingResponse(
        content=content,
        status_code=200,
        media_type="image/png"
    )


@images.post("/", dependencies=[Depends(IsAdmin.check)])
async def upload_image(
    file: UploadFile,
    clientS3: MinIoClient = Depends(),
    session: Session = Depends()
) -> ImageResponse:
    image = await ImageUploadUseCase(
        image_repo=ImageRepository(session)
    ).execute(file, clientS3)
    return image
