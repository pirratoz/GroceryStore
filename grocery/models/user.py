from uuid import uuid4

from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)

from grocery.enums import UserRole
from grocery.models.base_model import (
    BaseModel,
    bytea,
    uuid,
)


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid] = mapped_column(primary_key=True, unique=True, default=uuid4)
    role: Mapped[UserRole]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytea]

    cart = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
