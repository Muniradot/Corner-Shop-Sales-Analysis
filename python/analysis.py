"""
Corner Shop sales analysis (DEMO DATA - made-up shop).

What this script does, step by step:
1. Loads the two CSV files (products and sales)
2. Joins them, so every sale has a price and a cost
3. Works out revenue and profit
4. Finds the best sellers, monthly sales, and what needs reordering
5. Saves three charts into the images/ folder

Run it from the project folder:  python python/analysis.py
"""
import pandas as pd
import matplotlib.pyplot as plt

# ---- 1. Load the data
products = pd.read_csv("data/products.csv")
sales = pd.read_csv("data/sales.csv", parse_dates=["date"])

# ---- 2. Join sales to products (so each sale knows its price and cost)
df = sales.merge(products, on="product", how="left")

# Check: every sale should match a product
assert df["price"].notna().all(), "Some sales have a product that is not in products.csv"

# ---- 3. Revenue and profit for each sale
df["revenue"] = df["qty"] * df["price"]
df["profit"] = df["qty"] * (df["price"] - df["cost"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# ---- 4. Answer the shop owner's questions
total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
margin = total_profit / total_revenue

by_product = (
    df.groupby("product")
    .agg(units=("qty", "sum"), revenue=("revenue", "sum"), profit=("profit", "sum"))
    .sort_values("revenue", ascending=False)
)
by_month = df.groupby("month")["revenue"].sum()
by_category = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

# Stock left = opening stock minus everything sold
sold = df.groupby("product")["qty"].sum()
stock = products.set_index("product")
stock["units_sold"] = sold
stock["stock_left"] = stock["opening_stock"] - stock["units_sold"]
reorder = stock[stock["stock_left"] <= stock["reorder_level"]]

print(f"Total revenue: £{total_revenue:,.2f}")
print(f"Total profit:  £{total_profit:,.2f}  (margin {margin:.1%})")
print("\nTop 5 products by revenue:\n", by_product.head(5).round(2))
print("\nRevenue by month:\n", by_month.round(2))
print("\nRevenue by category:\n", by_category.round(2))
print("\nNeeds reordering:\n", reorder[["stock_left", "reorder_level"]])

# ---- 5. Charts
plt.style.use("seaborn-v0_8-whitegrid")
NAVY, GREY, RED = "#1F3A5F", "#B0B7C3", "#C0392B"

# Chart 1: products ranked by profit (the key one for the owner)
p = by_product.sort_values("profit")
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(p.index, p["profit"], color=[NAVY if i >= len(p) - 3 else GREY for i in range(len(p))])
top3 = list(p.index[-3:][::-1])
ax.set_title(f"{top3[0]}, {top3[1]} and {top3[2]} earn the most profit", fontsize=13, fontweight="bold")
ax.set_xlabel("Profit (£), Jul-Sep 2026")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("images/profit_by_product.png", dpi=150); plt.close()

# Chart 2: monthly revenue
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(by_month.index, by_month.values, color=NAVY)
ax.set_title("Monthly revenue", fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue (£)")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("images/monthly_revenue.png", dpi=150); plt.close()

# Chart 3: stock left vs reorder level for items that need reordering
fig, ax = plt.subplots(figsize=(7, 4.5))
x = range(len(reorder))
ax.bar([i - 0.2 for i in x], reorder["stock_left"], width=0.4, color=RED, label="Stock left")
ax.bar([i + 0.2 for i in x], reorder["reorder_level"], width=0.4, color=GREY, label="Reorder level")
ax.set_xticks(list(x)); ax.set_xticklabels(reorder.index, rotation=15)
ax.set_title(f"{len(reorder)} products need reordering", fontsize=14, fontweight="bold")
ax.legend(); ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("images/reorder_list.png", dpi=150); plt.close()
print("\nCharts saved to images/")
