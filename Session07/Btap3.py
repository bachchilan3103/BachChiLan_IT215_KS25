from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate):
    product = next((p for p in products_db if p["id"] == data.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")

    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Số lượng mua phải lớn hơn 0")
    if data.quantity > product["stock"]:
        raise HTTPException(status_code=400, detail="Sản phẩm không đủ số lượng trong kho")

    product["stock"] -= data.quantity

    order_id = len(orders_db) + 1
    total_price = data.quantity * product["price"]
    new_order = {
        "id": order_id,
        "product_id": product["id"],
        "quantity": data.quantity,
        "total_price": total_price
    }
    orders_db.append(new_order)
    return {"message": "Đơn hàng tạo thành công", "order": new_order}
