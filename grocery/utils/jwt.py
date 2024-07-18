from typing import Any
from datetime import (
    datetime,
    timezone,
    timedelta,
)

from jwt import (
    encode,
    decode,
)

from grocery.config import JWTConfig


class Jwt:
    @staticmethod
    def encode(
        payload: dict[str, Any],
        key: str = JWTConfig().PRIVATE_KEY_PATH.read_text(),
        algorithm: str = JWTConfig().ALGORITHM,
        exp: timedelta = timedelta(minutes=JWTConfig().ACCESS_TOKEN_EXP_MINUTES)
    ) -> str:
        current_time = datetime.now(timezone.utc)
        payload = payload | {
            "iat": current_time,
            "exp": current_time + exp
        }
        return encode(
            payload=payload,
            key=key,
            algorithm=algorithm
        )

    @staticmethod
    def decode(
        access_token: str, 
        key: str = JWTConfig().PUBLIC_KEY_PATH.read_text(),
        algorithm: str = JWTConfig().ALGORITHM
    ) -> Any:
        return decode(
            jwt=access_token,
            key=key,
            algorithms=[algorithm]
        )
