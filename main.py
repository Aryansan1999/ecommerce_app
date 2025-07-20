from fastapi import FastAPI
from routes import products, orders

app = FastAPI(title="Ecommerce FastAPI App")

app.include_router(products.router)
app.include_router(orders.router)
