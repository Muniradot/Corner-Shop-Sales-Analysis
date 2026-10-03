"""Loads the CSV files into a temporary SQLite database and runs sql/queries.sql.
Run from the project folder:  python python/run_sql.py
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
pd.read_csv("data/products.csv").to_sql("products", conn, index=False)
pd.read_csv("data/sales.csv").to_sql("sales", conn, index=False)

# Split the file into separate queries and run each one
queries = [q.strip() for q in open("sql/queries.sql").read().split(";") if "SELECT" in q]
for i, q in enumerate(queries, 1):
    print(f"--- Query {i} ---")
    print(pd.read_sql_query(q, conn).to_string(index=False), "\n")
