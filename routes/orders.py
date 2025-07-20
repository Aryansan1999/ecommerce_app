from fastapi import APIRouter
from models import OrderCreate, OrderOut
from database import db
from typing import List
from utils import paginate

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    order_dict = order.dict()
    result = await db.orders.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@router.get("/orders/{user_id}", response_model=dict)
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    query = {"userId": user_id}
    total = await db.orders.count_documents(query)
    cursor = db.orders.find(query).skip(offset).limit(limit)

    data = []
    async for order in cursor:
        items = []
        total_price = 0.0
        for item in order["items"]:
            product = await db.products.find_one({"id": item["productId"]})
            if product:
                items.append({
                    "productDetails": {
                        "name": product["name"],
                        "id": product["id"]
                    },
                    "qty": item["qty"]
                })
                total_price += item["qty"] * product["price"]
        data.append({
            "id": str(order["_id"]),
            "items": items,
            "total": total_price
        })

    return {
        "data": data,
        "page": paginate(limit, offset, total)
    }


@router.get("/orders", response_model=dict)
async def get_all_orders(limit: int = 10, offset: int = 0):
    total = await db.orders.count_documents({})
    cursor = db.orders.find({}).skip(offset).limit(limit)

    data = []
    async for order in cursor:
        items = []
        total_price = 0.0

        for item in order["items"]:
            product = await db.products.find_one({"id": item["productId"]})
            if product:
                items.append({
                    "productDetails": {
                        "id": product["id"],
                        "name": product["name"]
                    },
                    "qty": item["qty"]
                })
                total_price += item["qty"] * product["price"]

        data.append({
            "id": str(order["_id"]),
            "userId": order["userId"],
            "items": items,
            "total": total_price
        })

    return {
        "data": data,
        "page": paginate(limit, offset, total)
    }
