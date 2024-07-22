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
)


class SubCategory(BaseModel):
    __tablename__ = "subcategories"

    id: Mapped[uuid] = mapped_column(primary_key=True, unique=True, default=uuid4)
    category_id: Mapped[uuid] = mapped_column(ForeignKey("categories.id"))
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    image_id: Mapped[uuid] = mapped_column(ForeignKey("images.id"))

    category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")
    image = relationship("Image", back_populates="subcategory")
