from typing import Annotated
from uuid import UUID
import json

from fastapi import (
    HTTPException,
    APIRouter,
    UploadFile,
    Form,
    File,
    Depends,
)

from grocery.dependencies import (
    SessionReadOnly,
    Session,
    IsAdmin,
    MinIoClient,
)
from grocery.repositories import (
    CategoryRepository,
    ImageRepository,
)
from grocery.scheme.request import CategoryCreateRequest
from grocery.usecases import (
    CategoryGetAllUseCase,
    CategoryCreateUseCase,
    CategoryDeleteUseCase,
)
from grocery.scheme.response import (
    CategoryManyResponse,
    CategoryResponse,
)


categories = APIRouter()


@categories.get("/")
async def get_categories(
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> CategoryManyResponse:
    categories = await CategoryGetAllUseCase(
        category_repo=CategoryRepository(session)
    ).execute(limit, offset)
    return categories


@categories.post("/", dependencies=[Depends(IsAdmin.check)])
async def create_category(
    category_data: CategoryCreateRequest,
    session: Session = Depends()
) -> CategoryResponse:
    category = await CategoryCreateUseCase(
        category_repo=CategoryRepository(session),
        image_repo=ImageRepository(session)
    ).execute(category_data)
    return category


@categories.patch("/{category_id}", dependencies=[Depends(IsAdmin.check)])
async def partial_update_category(
    category_id: UUID,
    session: Session = Depends()
) -> CategoryResponse:
    return ...


@categories.delete("/{category_id}", dependencies=[Depends(IsAdmin.check)])
async def delete_template(
    category_id: UUID,
    session: Session = Depends()
) -> CategoryResponse:
    category = await CategoryDeleteUseCase(
        CategoryRepository(session)
    ).execute(category_id)
    return category
