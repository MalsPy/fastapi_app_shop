from typing import List
from uuid import UUID
from app.schemas import ProductSchemas, ProductCreate

# Пример фейковой базы данных — список продуктов
fake_products = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "Test",
        "description": "Test",
        "price": 10000,
        "in_stock": False,
    }
]


# Возвращает список схем
async def get_fake_db() -> List[ProductSchemas]:
    return [ProductSchemas(**item) for item in fake_products]


# Возвращает схему по UUID
async def get_fake_db_id(product_id: UUID) -> ProductSchemas | None:
    for item in fake_products:
        if str(item["id"]) == str(product_id):
            return ProductSchemas(**item)
    return None


async def add_new_product(request):
    fake_products.append(request.model_dump())
    print(fake_products)


async def update_product_fully(
    product_id: UUID, new_data: ProductSchemas | ProductCreate
) -> ProductSchemas | None:
    for i, item in enumerate(fake_products):
        if str(item["id"]) == str(product_id):
            updated_product = ProductSchemas(id=product_id, **new_data.model_dump())
            fake_products[i] = updated_product.model_dump()
            return updated_product
    return None


async def update_product_partially(
    product_id: UUID, updated_fields: dict
) -> ProductSchemas | None:
    for i, item in enumerate(fake_products):
        if str(item["id"]) == str(product_id):
            fake_products[i].update(updated_fields)
            return ProductSchemas(**fake_products[i])
    return None


async def delete_product_by_id(product_id: UUID) -> bool:
    for i, item in enumerate(fake_products):
        if str(item["id"]) == str(product_id):
            del fake_products[i]
            return True
    return False
