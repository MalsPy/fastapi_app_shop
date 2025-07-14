# app/fake_db.py

from typing import List
from app.schemas import ProductSchemas

# Пример фейковой базы данных — список продуктов
fake_products = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "Test",
        "description": "Test",
        "price": 1000,
        "in_stock": False,
    }
]


# Вот эту функцию ты импортируешь как Depends
def get_fake_db() -> list[ProductSchemas]:
    return fake_products
