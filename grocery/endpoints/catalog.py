from fastapi import (
    APIRouter,
    Depends,
)

from grocery.dependencies import SessionReadOnly
from grocery.usecases import (
    CatalogGetSubcategoriesUseCase,
    CatalogGetProductsUseCase,
    CatalogGetProductUseCase,
)
from grocery.repositories import (
    SubCategoryRepository,
    CategoryRepository,
    ProductRepository,
)
from grocery.scheme.response import (
    SubCategoryManyResponse,
    ProductManyResponse,
    ProductResponse,
)


catalog = APIRouter()


@catalog.get("/{category}/{subcategory}/{product}")
async def get_product(
    category: str,
    subcategory: str,
    product: str,
    session: SessionReadOnly = Depends()
) -> ProductResponse:
    product_item = await CatalogGetProductUseCase(
        category_repo=CategoryRepository(session),
        subcategory_repo=SubCategoryRepository(session),
        product_repo=ProductRepository(session)
    ).execute(
        slug_category=category,
        slug_subcategory=subcategory,
        slug_product=product
    )
    return product_item


@catalog.get("/{category}/{subcategory}")
async def get_products(
    category: str,
    subcategory: str,
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> ProductManyResponse:
    products = await CatalogGetProductsUseCase(
        category_repo=CategoryRepository(session),
        subcategory_repo=SubCategoryRepository(session),
        product_repo=ProductRepository(session)
    ).execute(
        slug_category=category,
        slug_subcategory=subcategory,
        limit=limit,
        offset=offset
    )
    return products


@catalog.get("/{category}")
async def get_subcategories(
    category: str,
    limit: int = 10,
    offset: int = 0,
    session: SessionReadOnly = Depends()
) -> SubCategoryManyResponse:
    subcategories = await CatalogGetSubcategoriesUseCase(
        category_repo=CategoryRepository(session),
        subcategory_repo=SubCategoryRepository(session)
    ).execute(
        slug_category=category,
        limit=limit,
        offset=offset
    )
    return subcategories
