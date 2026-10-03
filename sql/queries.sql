-- Corner Shop sales analysis (DEMO DATA - made-up shop)
-- Written for SQLite. Tables: products, sales (loaded from the CSV files in /data).

-- 1. Total revenue, profit and margin
SELECT
    ROUND(SUM(s.qty * p.price), 2)                         AS total_revenue,
    ROUND(SUM(s.qty * (p.price - p.cost)), 2)              AS total_profit,
    ROUND(SUM(s.qty * (p.price - p.cost)) * 100.0
          / SUM(s.qty * p.price), 1)                       AS margin_pct
FROM sales s
JOIN products p ON p.product = s.product;

-- 2. Top 5 products by revenue
SELECT
    p.product,
    SUM(s.qty)                              AS units_sold,
    ROUND(SUM(s.qty * p.price), 2)          AS revenue
FROM sales s
JOIN products p ON p.product = s.product
GROUP BY p.product
ORDER BY revenue DESC
LIMIT 5;

-- 3. Revenue by month
SELECT
    strftime('%Y-%m', s.date)               AS month,
    ROUND(SUM(s.qty * p.price), 2)          AS revenue
FROM sales s
JOIN products p ON p.product = s.product
GROUP BY month
ORDER BY month;

-- 4. Revenue by category
SELECT
    p.category,
    ROUND(SUM(s.qty * p.price), 2)          AS revenue
FROM sales s
JOIN products p ON p.product = s.product
GROUP BY p.category
ORDER BY revenue DESC;

-- 5. Products that need reordering (stock left is at or below the reorder level)
SELECT
    p.product,
    p.opening_stock - COALESCE(SUM(s.qty), 0)   AS stock_left,
    p.reorder_level
FROM products p
LEFT JOIN sales s ON s.product = p.product
GROUP BY p.product
HAVING stock_left <= p.reorder_level
ORDER BY stock_left;
