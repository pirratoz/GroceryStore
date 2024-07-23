from uuid import UUID

from fastapi.responses import Response
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
    CategoryRepository,
    ProductRepository,
    ImageRepository,
)
from grocery.usecases import (
    SubCategoryPartialUpdateUseCase,
    SubCategoryGetAllUseCase,
    SubCategoryCreateUseCase,
    SubCategoryDeleteUseCase,
    SubCategoryGetProductsBySlugUseCase,
)
from grocery.scheme.request import (
    SubCategoryPartialUpdateRequest,
    SubCategoryCreateRequest,
)
from grocery.scheme.response import (
    SubCategoryManyResponse,
    ProductManyResponse,
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
        subcategory_repo=SubCategoryRepository(session)
    ).execute(limit, offset)
    return subcategories


@subcategories.get("/{subcategory}")
async def get_products(
    category: str,
    subcategory: str,
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> ProductManyResponse:
    return await SubCategoryGetProductsBySlugUseCase(
        category_repo=CategoryRepository(session),
        subcategory_repo=SubCategoryRepository(session),
        product_repo=ProductRepository(session)
    ).execute(
        slug_category=category,
        slug_subcategory=subcategory,
        limit=limit,
        offset=offset
    )


@subcategories.post(
    path="/",
    status_code=201,
    dependencies=[Depends(IsAdmin.check)]
)
async def create_subcategory(
    data: SubCategoryCreateRequest,
    session: Session = Depends()
) -> SubCategoryResponse:
    subcategory = await SubCategoryCreateUseCase(
        subcategory_repo=SubCategoryRepository(session),
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
        subcategory_repo=SubCategoryRepository(session),
        image_repo=ImageRepository(session)
    ).execute(subcategory_id, data)
    return subcategory


@subcategories.delete(
    path="/{subcategory_id}",
    status_code=204,
    dependencies=[Depends(IsAdmin.check)]
)
async def delete_subcategory(
    subcategory_id: UUID,
    session: Session = Depends()
) -> Response:
    await SubCategoryDeleteUseCase(
        subcategory_repo=SubCategoryRepository(session)
    ).execute(subcategory_id)
    return Response(status_code=204)
