import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==============================
# PROJECT PATH
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VISUALIZATION_DIR = BASE_DIR / "visualization"

VISUALIZATION_DIR.mkdir(exist_ok=True)


# ==============================
# LOAD DATASET
# ==============================

orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
payments = pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")


# ==============================
# DATA CHECK
# ==============================

print("Orders:", orders.shape)
print("Customers:", customers.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Products:", products.shape)

# ==============================
# ORDER STATUS ANALYSIS
# ==============================

status = (
    orders
    .groupby("order_status")
    .agg(order_count=("order_id", "count"))
    .sort_values("order_count", ascending=False)
)

print("\nOrder Status:")
print(status)

# ==============================
# ORDER STATUS VISUALIZATION
# ==============================

plt.figure(figsize=(10, 5))

plt.bar(
    status.index,
    status["order_count"]
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(VISUALIZATION_DIR / "order_status.png")

plt.show()

# ==============================
# CITY ANALYSIS
# ==============================

city_orders = (
    customers
    .groupby("customer_city")
    .agg(order_count=("customer_id", "count"))
    .sort_values("order_count", ascending=False)
)

print("\nTop 10 Cities:")
print(city_orders.head(10))

# ==============================
# PRODUCT CATEGORY ANALYSIS
# ==============================

product_sales = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

category_sales = (
    product_sales
    .groupby("product_category_name")
    .agg(
        total_items=("product_id", "count")
    )
    .sort_values("total_items", ascending=False)
)

print("\nTop 10 Product Categories:")
print(category_sales.head(10))

# ==============================
# PRODUCT CATEGORY VISUALIZATION
# ==============================

top_categories = category_sales.head(10)

plt.figure(figsize=(10, 5))

plt.bar(
    top_categories.index,
    top_categories["total_items"]
)

plt.title("Top 10 Product Categories by Items Sold")
plt.xlabel("Product Category")
plt.ylabel("Items Sold")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    VISUALIZATION_DIR / "top_product_categories.png"
)

plt.show()

# ==============================
# PAYMENT ANALYSIS
# ==============================

payment_analysis = (
    payments
    .groupby("payment_type")
    .agg(
        total_payments=("payment_type", "count"),
        total_revenue=("payment_value", "sum")
    )
    .sort_values("total_payments", ascending=False)
)

print("\nPayment Analysis:")
print(payment_analysis)

# ==============================
# CUSTOMER REVIEW ANALYSIS
# ==============================

review_analysis = (
    reviews
    .groupby("review_score")
    .agg(
        total_reviews=("review_score", "count")
    )
    .sort_index(ascending=False)
)

print("\nCustomer Review Analysis:")
print(review_analysis)

# ==============================
# REVIEW VISUALIZATION
# ==============================

plt.figure(figsize=(8, 5))

plt.bar(
    review_analysis.index.astype(str),
    review_analysis["total_reviews"]
)

plt.title("Customer Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")

plt.tight_layout()

plt.savefig(
    VISUALIZATION_DIR / "customer_reviews.png"
)

plt.show()

# ==============================
# PAYMENT VISUALIZATION
# ==============================

plt.figure(figsize=(10, 5))

plt.bar(
    payment_analysis.index,
    payment_analysis["total_payments"]
)

plt.title("Payment Method Usage")
plt.xlabel("Payment Method")
plt.ylabel("Number of Payments")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    VISUALIZATION_DIR / "payment_methods.png"
)

plt.show()

# ==============================
# ACTUAL ORDERS BY CITY
# ==============================

city_order_data = customers.merge(
    orders[["order_id", "customer_id"]],
    on="customer_id",
    how="inner"
)

city_actual_orders = (
    city_order_data
    .groupby("customer_city")
    .agg(order_count=("order_id", "count"))
    .sort_values("order_count", ascending=False)
)

print("\nTop 10 Cities by Actual Orders:")
print(city_actual_orders.head(10))

# ==============================
# CITY VISUALIZATION
# ==============================

top_cities = city_orders.head(10)

plt.figure(figsize=(10, 5))

plt.bar(
    top_cities.index,
    top_cities["order_count"]
)

plt.title("Top 10 Cities by Customer Count")
plt.xlabel("City")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(VISUALIZATION_DIR / "top_cities.png")

plt.show()

# ==============================
# ACTUAL ORDERS VISUALIZATION
# ==============================

top_order_cities = city_actual_orders.head(10)

plt.figure(figsize=(10, 5))

plt.bar(
    top_order_cities.index,
    top_order_cities["order_count"]
)

plt.title("Top 10 Cities by Actual Orders")
plt.xlabel("City")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    VISUALIZATION_DIR / "top_cities_actual_orders.png"
)

plt.show()
