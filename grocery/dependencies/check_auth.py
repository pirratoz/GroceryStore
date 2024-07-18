from typing import Any
from abc import ABC

from fastapi import (
    HTTPException,
    Depends,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt.exceptions import (
    InvalidTokenError,
    ExpiredSignatureError,
)

from grocery.dependencies.postgresql_session import SessionReadOnly
from grocery.utils import Jwt


class Auth(ABC):
    security = HTTPBearer()

    # for openapi docs
    def __init__(self,
        credentials: HTTPAuthorizationCredentials = Depends(security) 
    ) -> None:
        ...

    async def auth(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: SessionReadOnly = Depends()
    ) -> dict[str, Any]:
        payload: dict[str, Any]

        try:
            payload = Jwt.decode(access_token=credentials.credentials)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Expired signature"
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Token is invalid"
            )

        return payload
