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
from grocery.repositories import CategoryRepository
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
    return ...


@categories.post("/", dependencies=[Depends(IsAdmin.check)])
async def create_category(
    session: Session = Depends()
) -> CategoryResponse:
    return ...


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
    return ...
