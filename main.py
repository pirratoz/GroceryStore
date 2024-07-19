from fastapi import FastAPI
from uvicorn import run as uvicorn_run

from grocery.dependencies import (
    Session,
    SessionReadOnly,
    DatabaseConnector,
    Auth,
    IsAdmin,
    MinIoConnector,
    MinIoClient,
)
from grocery.docs import Tags
from grocery.endpoints import (
    users,
    jwt,
    categories,
    images,
)


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


def main() -> None:
    app = FastAPI()
    postgresql = DatabaseConnector()
    s3 = MinIoConnector()

    setup_dependency(app, postgresql, s3)
    include_endpoints(app)

    uvicorn_run(app)


if __name__ == "__main__":
    main()
