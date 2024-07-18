from uuid import uuid4

from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)

from grocery.models.base_model import (
    BaseModel,
    uuid,
)


class Image(BaseModel):
    __tablename__ = "images"

    id: Mapped[uuid] = mapped_column(primary_key=True, unique=True, default_factory=uuid4)
    filename: Mapped[str] = mapped_column(unique=True)

    product = relationship("Product", back_populates="image")
    category = relationship("Category", back_populates="image")
    subcategory = relationship("SubCategory", back_populates="image")
