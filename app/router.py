from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from uuid import UUID

from app.schemas import ProductSchemas, ProductCreate
from app.fake_db import (
    get_fake_db,
    get_fake_db_id,
    add_new_product,
    update_product_fully,
    update_product_partially,
    delete_product_by_id,
)

router = APIRouter(prefix="/product", tags=["Products 📦"])


@router.get("/get_all", response_model=List[ProductSchemas])
async def get_product_all(
    db: Annotated[List[ProductSchemas], Depends(get_fake_db)],
) -> List[ProductSchemas]:
    return db


@router.get("/get_id/{id}", response_model=ProductSchemas)
async def get_product_id(id: UUID):
    product = await get_fake_db_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/post", response_model=ProductSchemas)
async def post_product(add_product: ProductCreate):
    from uuid import uuid4

    product = ProductSchemas(id=uuid4(), **add_product.model_dump())
    await add_new_product(product)
    return product


@router.patch("/patch/{id}", response_model=ProductSchemas)
async def patch_product(id: UUID, updated_fields: dict):
    product = await update_product_partially(id, updated_fields)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/put/{id}", response_model=ProductSchemas)
async def put_product(id: UUID, product_data: ProductCreate):
    updated_product = await update_product_fully(id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/delete/{id}")
async def delete_product(id: UUID):
    deleted = await delete_product_by_id(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "message": f"Product {id} deleted"}
