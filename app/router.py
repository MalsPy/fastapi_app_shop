from fastapi import APIRouter, Depends
from typing import Annotated, List
from app.schemas import ProductSchemas
from app.fake_db import get_fake_db  # допустим, это функция-депенденси

router = APIRouter(prefix="/product", tags=["Products 📦"])


@router.get("/get_all", response_model=List[ProductSchemas])
async def get_product_all(
    db: Annotated[list[ProductSchemas], Depends(get_fake_db)],
) -> List[ProductSchemas]:
    return db


@router.get("/get_id", response_model=List[ProductSchemas])
async def get_product_id():
    return {"success": "ok"}


@router.post("/post")
async def post_product():
    return {"success": "ok"}


@router.patch("/patch")
async def patch_product():
    return {"success": "ok"}


@router.put("/put")
async def put_product():
    return {"success": "ok"}


@router.delete("/delete")
async def delete_product():
    return {"success": "ok"}
