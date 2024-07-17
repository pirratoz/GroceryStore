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
from grocery.utils.jwt import decode_jwt


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
            payload = decode_jwt(access_token=credentials.credentials)
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
