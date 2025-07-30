from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from uuid import UUID
from uuid import uuid4

from sqlalchemy import delete
from starlette.status import HTTP_404_NOT_FOUND
from starlette.types import HTTPExceptionHandler

from app.db.models import Product
from app.schemas import ProductSchemas, ProductCreate
from app.fake_db import (
    get_fake_db,
    get_fake_db_id,
    add_new_product,
    update_product_fully,
    update_product_partially,
    delete_product_by_id,
)
from app.db.queries import Products

router = APIRouter(prefix="/products", tags=["Products 📦"])

# --- Postgres db ---


@router.get("/new_get_all", response_model=List[ProductSchemas])
async def get_all_products():
    products = await Products.get_all_products()
    return products


@router.get("/get_id/{id}", response_model=ProductSchemas)
async def get_product_by_id(id: UUID):
    product = await Products.get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/post", response_model=ProductSchemas)
async def post_product(add_product: ProductCreate):
    product = await Products.create_product(add_product)
    return product


@router.patch("/pathch/{id}", response_model=ProductSchemas)
async def patch_product(id: UUID, updated_fields: dict):
    product = await Products.update_product_partially(id, updated_fields)
    if not product:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.put("/put/{id}", response_model=ProductSchemas)
async def put_product(id: UUID, product_data: ProductCreate):
    update_product = await Products.update_product_fully(id, product_data)
    if not update_product:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Products not fount")
    return update_product


@router.delete("/delete/{id}")
async def delete_product(id: UUID):
    deleted = await Products.delete_product_by_id(id)
    if not deleted:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Product not found")
    return {"success": True, "message": f"Product {id} deleted"}


# ---Fake db ---


# @router.get("/get_all", response_model=List[ProductSchemas])
# async def get_product_all(
#     db: Annotated[List[ProductSchemas], Depends(get_fake_db)],
# ) -> List[ProductSchemas]:
#     return db
#
#
# @router.get("/get_id/{id}", response_model=ProductSchemas)
# async def get_product_id(id: UUID):
#     product = await get_fake_db_id(id)
#     if not product:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
#         )
#     return product
#
#
# @router.post("/post", response_model=ProductSchemas)
# async def post_product(add_product: ProductCreate):
#
#     product = ProductSchemas(id=uuid4(), **add_product.model_dump())
#     await add_new_product(product)
#     return product
#
#
# @router.patch("/patch/{id}", response_model=ProductSchemas)
# async def patch_product(id: UUID, updated_fields: dict):
#     product = await update_product_partially(id, updated_fields)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product
#
#
# @router.put("/put/{id}", response_model=ProductSchemas)
# async def put_product(id: UUID, product_data: ProductCreate):
#     updated_product = await update_product_fully(id, product_data)
#     if not updated_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return updated_product
#
#
# @router.delete("/delete/{id}")
# async def delete_product(id: UUID):
#     deleted = await delete_product_by_id(id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"success": True, "message": f"Product {id} deleted"}
