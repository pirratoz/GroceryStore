from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)

from grocery.models.base_model import (
    BaseModel,
    uuid,
    int_64,
)


class Product(BaseModel):
    __tablename__ = "products"

    id: Mapped[uuid] = mapped_column(primary_key=True, unique=True, index=True, default=uuid4)
    subcategory_id: Mapped[uuid] = mapped_column(ForeignKey("subcategories.id"))
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True, index=True)
    image_id: Mapped[uuid] = mapped_column(ForeignKey("images.id"))

    price: Mapped[int_64]
    weight_gramm: Mapped[int_64]

    subcategory = relationship("SubCategory", back_populates="products")
    image = relationship("Image", back_populates="product")
    carts = relationship("Cart", back_populates="product")
