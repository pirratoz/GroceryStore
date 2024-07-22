from uuid import UUID

from fastapi.responses import JSONResponse
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
    ImageRepository,
)
from grocery.usecases import (
    CategoryGetSubcategoriesBySlugUseCase,
    CategoryPartialUpdateUseCase,
    CategoryGetAllUseCase,
    CategoryCreateUseCase,
    CategoryDeleteUseCase,
)
from grocery.scheme.request import (
    CategoryPartialUpdateRequest,
    CategoryCreateRequest,
)
from grocery.scheme.response import (
    SubCategoryManyResponse,
    CategoryManyResponse,
    CategoryResponse,
)


categories = APIRouter()


@categories.get("/{category}")
async def get_subcategories(
    category: str,
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> SubCategoryManyResponse:
    subcategories = await CategoryGetSubcategoriesBySlugUseCase(
        category_repo=CategoryRepository(session),
        subcategory_repo=SubCategoryRepository(session)
    ).execute(
        slug_category=category,
        limit=limit,
        offset=offset
    )
    return subcategories


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
    data: CategoryPartialUpdateRequest,
    session: Session = Depends()
) -> CategoryResponse:
    category = await CategoryPartialUpdateUseCase(
        CategoryRepository(session),
        ImageRepository(session)
    ).execute(category_id, data)
    return category


@categories.delete("/{category_id}", dependencies=[Depends(IsAdmin.check)])
async def delete_category(
    category_id: UUID,
    session: Session = Depends()
) -> CategoryResponse:
    await CategoryDeleteUseCase(
        CategoryRepository(session)
    ).execute(category_id)
    return JSONResponse(content={}, status_code=204)
