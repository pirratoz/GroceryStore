from fastapi import FastAPI
from uvicorn import run as uvicorn_run

from grocery.dependencies import (
    Session,
    SessionReadOnly,
    DatabaseConnector,
    Auth,
)
from grocery.docs import Tags
from grocery.endpoints import (
    users,
    jwt,
)


def setup_dependency(app: FastAPI, db: DatabaseConnector) -> None:
    app.dependency_overrides[Session] = db.get_session
    app.dependency_overrides[SessionReadOnly] = db.get_session_read_only
    app.dependency_overrides[Auth] = Auth.auth


def include_endpoints(app: FastAPI) -> None:
    app.include_router(users, prefix="/users", tags=[Tags.users])
    app.include_router(jwt, prefix="/jwt", tags=[Tags.jwt])


def main() -> None:
    app = FastAPI()
    postgresql = DatabaseConnector()

    setup_dependency(app, postgresql)
    include_endpoints(app)
    
    uvicorn_run(app)


if __name__ == "__main__":
    main()
