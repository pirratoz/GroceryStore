from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class MinIoConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MINIO_",
        extra="ignore",
    )

    HOST: str
    USER: str
    PASS: str
    BUCKET: str
    ACCESS_KEY: str
    SECRET_KEY: str
