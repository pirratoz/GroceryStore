from typing_extensions import Annotated
from sqlalchemy.orm import (
    DeclarativeBase,
    registry
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import (
    DateTime,
    BigInteger,
    Integer,
    String,
    Uuid,
)


int_32 = Annotated[Integer, "int_32"]
int_64 = Annotated[BigInteger, "int_64"]
uuid = Annotated[Uuid, "uuid"]
bytea = Annotated[BYTEA, "bytea"]

str_256 = Annotated[String, 256]

date_time = Annotated[DateTime, "date_time"]


class BaseModel(DeclarativeBase):
    registry = registry(
        type_annotation_map = {
            str_256: String(256),
            int_32: Integer(),
            int_64: BigInteger(),
            date_time: DateTime(),
            uuid: Uuid(),
            bytea: BYTEA(),
        }
    )
