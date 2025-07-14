from pydantic import BaseModel, Field
from uuid import UUID


class ProductSchemas(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    price: float
    in_stock: bool | None = False
