from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

# Create FastAPI app

app = FastAPI(title="E-commerce API", version="1.0")

# -----------------------------

# Product Data

# -----------------------------

products = [
{"id": 1, "name": "Wireless Mouse", "price": 799, "category": "Electronics", "in_stock": True},
{"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
{"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
{"id": 4, "name": "Office Chair", "price": 4999, "category": "Furniture", "in_stock": False},
{"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
{"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
{"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

feedback = []
orders = []

# -----------------------------

# Pydantic Models

# -----------------------------

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

# -----------------------------

# Home Route

# -----------------------------

@app.get("/")
def home():
    return {"message": "Welcome to My E-commerce API"}

# -----------------------------

# Assignment 1 Endpoints

# -----------------------------

# Show all products

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# Filter by category

@app.get("/products/category/{category_name}")
def get_category(category_name: str):
    result = [
        p for p in products
        if p["category"].lower() == category_name.lower()
    ]

    return {
        "category": category_name,
        "products": result
    }

# Show in-stock products

@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"]]

    return {
        "available_products": available,
        "count": len(available)
    }

# Store summary

@app.get("/store/summary")
def store_summary():
    in_stock = len([p for p in products if p["in_stock"]])
    out_of_stock = len(products) - in_stock
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }

# Search products

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

# Best deals

@app.get("/products/deals")
def product_deals():
    cheapest = min(products, key=lambda x: x["price"])
    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "cheapest_product": cheapest,
        "most_expensive_product": most_expensive
    }

# -----------------------------

# Assignment 2 Endpoints

# -----------------------------

# Product filtering

@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None)
):
    result = products

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    return {
        "filtered_products": result,
        "count": len(result)
    }

# Get only product price

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}

# Customer feedback

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }

# Product summary dashboard

@app.get("/products/summary")
def product_summary():
    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set(p["category"] for p in products))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }

# Bulk order API

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:
        product = next(
            (p for p in products if p["id"] == item.product_id),
            None
        )

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })

        elif not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })

        else:
            subtotal = product["price"] * item.quantity

            grand_total += subtotal

            confirmed.append({
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal
            })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# -----------------------------

# Bonus – Order Status Tracker

# -----------------------------

@app.post("/orders")
def place_order(product_id: int, quantity: int):
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return {"error": "Product not found"}

    order = {
        "order_id": len(orders) + 1,
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "status": "pending"
    }

    orders.append(order)

    return {
        "message": "Order placed successfully",
        "order": order
    }

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return {"order": order}

    return {"error": "Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"

            return {
                "message": "Order confirmed",
                "order": order
            }

    return {"error": "Order not found"}
