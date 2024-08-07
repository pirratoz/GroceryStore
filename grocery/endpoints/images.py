from typing import Literal
from uuid import UUID

from fastapi.responses import StreamingResponse
from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
)

from grocery.scheme.response import ImageResponse
from grocery.repositories import ImageRepository
from grocery.dependencies import (
    SessionReadOnly,
    MinIoClient,
    Session,
    IsAdmin,
)
from grocery.usecases import (
    ImageUploadUseCase,
    ImageStreamUseCase,
)


images = APIRouter()


@images.get("/{size}/{image_id}")
async def download_image(
    size: Literal["lg", "md", "sm"],
    image_id: UUID,
    clientS3: MinIoClient = Depends(),
    session: SessionReadOnly = Depends()
) -> StreamingResponse:
    content = await ImageStreamUseCase(
        image_repo=ImageRepository(session)
    ).execute(
        size=size,
        image_id=image_id,
        clientS3=clientS3
    )
    return StreamingResponse(
        content=content,
        status_code=200,
        media_type="image/png"
    )


@images.post(
    path="/",
    status_code=201,
    dependencies=[Depends(IsAdmin.check)]
)
async def upload_image(
    file: UploadFile,
    clientS3: MinIoClient = Depends(),
    session: Session = Depends()
) -> ImageResponse:
    image = await ImageUploadUseCase(
        image_repo=ImageRepository(session)
    ).execute(file, clientS3)
    return image
