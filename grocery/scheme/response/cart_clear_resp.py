from pydantic import BaseModel


class CartClearResponse(BaseModel):
    cleared: bool
