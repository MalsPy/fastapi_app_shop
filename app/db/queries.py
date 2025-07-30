from sqlalchemy import False_, select
from uuid import UUID, uuid4

from sqlalchemy.engine import result
from sqlalchemy.orm import session
from app.db.models import Product, Base
from app.db.database import async_engine, async_session_factory
from app.db.models import Product
from app.fake_db import delete_product_by_id
from app.schemas import ProductCreate


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class Products:
    @staticmethod
    async def get_all_products():
        async with async_session_factory() as session:
            query = select(Product)
            result = await session.execute(query)
            products = result.scalars().all()
            return products

    @staticmethod
    async def create_product(product_data: ProductCreate):
        async with async_session_factory() as session:
            product = Product(id=uuid4(), **product_data.model_dump())
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product

    @staticmethod
    async def get_product_by_id(product_id: UUID):
        async with async_session_factory() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()
            return product

    @staticmethod
    async def update_product_fully(product_id: UUID, new_data: ProductCreate):
        async with async_session_factory() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()
            if not product:
                return None
            for key, value in new_data.model_dump().items():
                setattr(product, key, value)
            await session.commit()
            await session.refresh(product)
            return product

    @staticmethod
    async def update_product_partially(product_id: UUID, update_data: dict):
        async with async_session_factory() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()
            if not product:
                return None
            for key, value in update_data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            await session.commit()
            await session.refresh(product)
            return product

    @staticmethod
    async def delete_product_by_id(product_id: UUID) -> bool:
        async with async_session_factory() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()
            if not product:
                return False
            await session.delete(product)
            await session.commit()
            return True
