from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="JWT_",
        extra="ignore",
    )

    PUBLIC_KEY_PATH: Path
    PRIVATE_KEY_PATH: Path
    ACCESS_TOKEN_EXP_MINUTES: int
    ALGORITHM: str
