from uvicorn import run as uvicorn_run
from fastapi import FastAPI

from grocery.dependencies import (
    DatabaseConnector,
    SessionReadOnly,
    MinIoConnector,
    MinIoClient,
    Session,
    IsAdmin,
    Auth,
)
from grocery.endpoints import (
    subcategories,
    categories,
    products,
    images,
    users,
    jwt,
)
from grocery.docs import Tags


def setup_dependency(
    app: FastAPI,
    db: DatabaseConnector,
    s3: MinIoConnector,
) -> None:
    app.dependency_overrides[Session] = db.get_session
    app.dependency_overrides[SessionReadOnly] = db.get_session_read_only
    app.dependency_overrides[Auth] = Auth.auth
    app.dependency_overrides[IsAdmin] = IsAdmin.check
    app.dependency_overrides[MinIoClient] = s3.get_client


def include_endpoints(app: FastAPI) -> None:
    app.include_router(users, prefix="/users", tags=[Tags.users])
    app.include_router(jwt, prefix="/jwt", tags=[Tags.jwt])
    app.include_router(categories, prefix="/categories", tags=[Tags.categories])
    app.include_router(images, prefix="/api/images", tags=[Tags.images])
    app.include_router(subcategories, prefix="/subcategories", tags=[Tags.subcategories])
    app.include_router(products, prefix="/products", tags=[Tags.products])    


def main() -> None:
    app = FastAPI()
    postgresql = DatabaseConnector()
    s3 = MinIoConnector()

    setup_dependency(app, postgresql, s3)
    include_endpoints(app)

    uvicorn_run(app)


if __name__ == "__main__":
    main()
