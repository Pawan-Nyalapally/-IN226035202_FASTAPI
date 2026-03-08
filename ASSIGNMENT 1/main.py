from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(title="E-commerce API", version="1.0")

# Product data
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 799, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Office Chair", "price": 4999, "category": "Furniture", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to My E-commerce API"}

# Q1 – Show all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# Q2 – Filter by category
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

# Q3 – Show in-stock products
@app.get("/products/instock")
def get_instock():

    available = [p for p in products if p["in_stock"]]

    return {
        "available_products": available,
        "count": len(available)
    }

# Q4 – Store summary
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

# Q5 – Search products
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

# Bonus – Best deals
@app.get("/products/deals")
def product_deals():

    cheapest = min(products, key=lambda x: x["price"])
    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "cheapest_product": cheapest,
        "most_expensive_product": most_expensive
    }
