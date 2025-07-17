from pydantic import BaseModel
from uuid import UUID


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: bool | None = False


class ProductSchemas(ProductCreate):
    id: UUID
