from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class PostgreSqlConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PG_",
        extra="ignore",
    )

    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str
    POOL_SIZE: int

    @property
    def DSN(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.HOST,
            port=self.PORT,
            username=self.USER,
            password=self.PASS,
            path=self.NAME
        ).unicode_string()
