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


class Category(BaseModel):
    __tablename__ = "categories"

    id: Mapped[uuid] = mapped_column(primary_key=True, unique=True, default_factory=uuid4)
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    image_id: Mapped[uuid] = mapped_column(ForeignKey("images.id"))

    subcategories = relationship("SubCategory", back_populates="subcategories")
    image = relationship("Image", back_populates="category")
