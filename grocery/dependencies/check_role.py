from abc import ABC

from fastapi import (
    Depends,
    HTTPException,
)

from grocery.dependencies.check_auth import Auth


class IsAdmin(ABC):
    async def check(auth: Auth = Depends()) -> bool:
        if auth["role"] in {"admin"}:
            return True
        raise HTTPException(
            status_code=403,
            detail="Have not permission"
        )
