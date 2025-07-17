from fastapi import FastAPI
from app.router import router as products_router

app = FastAPI()

app.include_router(products_router)


@app.get("/")
async def home():
    return {"Hello": "Welcome"}
