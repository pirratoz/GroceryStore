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
    ProductRepository,
    ImageRepository,
)
from grocery.usecases import (
    ProductPartialUpdateUseCase,
    ProductGetAllUseCase,
    ProductDeleteUseCase,
    ProductCreateUseCase,
)
from grocery.scheme.request import (
    ProductPartialUpdateRequest,
    ProductCreateRequest,
)
from grocery.scheme.response import (
    ProductManyResponse,
    ProductResponse,
)


products = APIRouter()


@products.get("/")
async def get_products(
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> ProductManyResponse:
    products = await ProductGetAllUseCase(
        product_repo=ProductRepository(session)
    ).execute(limit, offset)
    return products


@products.post("/", dependencies=[Depends(IsAdmin.check)])
async def create_product(
    data: ProductCreateRequest,
    session: Session = Depends()
) -> ProductResponse:
    product = await ProductCreateUseCase(
        subcategory_repo=SubCategoryRepository(session),
        product_repo=ProductRepository(session),
        image_repo=ImageRepository(session)
    ).execute(data)
    return product


@products.patch("/{product_id}", dependencies=[Depends(IsAdmin.check)])
async def partial_update_product(
    product_id: UUID,
    data: ProductPartialUpdateRequest,
    session: Session = Depends()
) -> ProductResponse:
    product = await ProductPartialUpdateUseCase(
        subcategory_repo=SubCategoryRepository(session),
        product_repo=ProductRepository(session),
        image_repo=ImageRepository(session)
    ).execute(product_id, data)
    return product


@products.delete("/{product_id}", dependencies=[Depends(IsAdmin.check)])
async def delete_product(
    product_id: UUID,
    session: Session = Depends()
) -> ProductResponse:
    product = await ProductDeleteUseCase(
        product_repo=ProductRepository(session),
        image_repo=ImageRepository(session)
    ).execute(product_id)
    return product
