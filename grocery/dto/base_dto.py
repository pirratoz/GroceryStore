from typing import (
    Iterable,
    TypeVar,
    Any,
)

from pydantic import BaseModel as PydanticBaseModel


ModelDto = TypeVar("ModelDto", bound="BaseModelDto")


class BaseModelDto(PydanticBaseModel):
    class Config:
        from_attributes = True
        extra = "allow"

    @classmethod
    def one_from_orm(cls: type[ModelDto], item: Any | None) -> ModelDto | None:
        return None if item is None else cls.model_validate(item)

    @classmethod
    def many_from_orm(cls: type[ModelDto], items: Iterable[Any]) -> list[ModelDto]:
        return [cls.model_validate(item) for item in items]
