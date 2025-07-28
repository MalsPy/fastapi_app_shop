from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.router import router as products_router
from app.db.queries import create_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print("Base clear")
    await create_tables()
    print("Read base for work")
    yield
    print("OFF")


app = FastAPI(lifespan=lifespan)

app.include_router(products_router)


@app.get("/")
async def home():
    return {"Hello": "Welcome"}
