from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from grocery.dependencies import (
    SessionReadOnly,
    Session,
    IsAdmin,
)
from grocery.repositories import (
    SubCategoryRepository,
    ImageRepository,
)
from grocery.scheme.request import (
    SubCategoryCreateRequest,
    SubCategoryPartialUpdateRequest,
)
from grocery.usecases import (
    SubCategoryGetAllUseCase,
    SubCategoryCreateUseCase,
    SubCategoryDeleteUseCase,
    SubCategoryPartialUpdateUseCase,
)
from grocery.scheme.response import (
    SubCategoryManyResponse,
    SubCategoryResponse,
)


subcategories = APIRouter()


@subcategories.get("/")
async def get_subcategories(
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> SubCategoryManyResponse:
    subcategories = await SubCategoryGetAllUseCase(
        category_repo=SubCategoryRepository(session)
    ).execute(limit, offset)
    return subcategories


@subcategories.post("/", dependencies=[Depends(IsAdmin.check)])
async def create_subcategory(
    data: SubCategoryCreateRequest,
    session: Session = Depends()
) -> SubCategoryResponse:
    subcategory = await SubCategoryCreateUseCase(
        category_repo=SubCategoryRepository(session),
        image_repo=ImageRepository(session)
    ).execute(data)
    return subcategory


@subcategories.patch("/{subcategory_id}", dependencies=[Depends(IsAdmin.check)])
async def partial_update_subcategory(
    subcategory_id: UUID,
    data: SubCategoryPartialUpdateRequest,
    session: Session = Depends()
) -> SubCategoryResponse:
    subcategory = await SubCategoryPartialUpdateUseCase(
        SubCategoryRepository(session),
        ImageRepository(session)
    ).execute(subcategory_id, data)
    return subcategory


@subcategories.delete("/{subcategory_id}", dependencies=[Depends(IsAdmin.check)])
async def delete_subcategory(
    subcategory_id: UUID,
    session: Session = Depends()
) -> SubCategoryResponse:
    subcategory = await SubCategoryDeleteUseCase(
        SubCategoryRepository(session)
    ).execute(subcategory_id)
    return subcategory
