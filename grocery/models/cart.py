from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)

from grocery.models.base_model import (
    BaseModel,
    int_32,
    uuid,
)


class Cart(BaseModel):
    __tablename__ = "carts"

    id: Mapped[uuid] = mapped_column(primary_key=True, unique=True, default=uuid4)
    user_id: Mapped[uuid] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[uuid] = mapped_column(ForeignKey("products.id"))
    count: Mapped[int_32]

    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="carts")
