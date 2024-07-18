from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)

from grocery.models.base_model import (
    BaseModel,
    uuid,
    int_32,
)


class Cart(BaseModel):
    __tablename__ = "carts"

    id: Mapped[uuid] = mapped_column(primary_key=True)
    user_id: Mapped[uuid] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[uuid] = mapped_column(ForeignKey("products.id"))
    count: Mapped[int_32]

    user = relationship("Cart", back_populates="cart")
    product = relationship("Product", back_populates="carts")
