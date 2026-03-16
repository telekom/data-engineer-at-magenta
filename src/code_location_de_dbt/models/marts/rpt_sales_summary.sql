-- Mart model: sales summary report
--
-- This model is the final reporting layer. It should be directly queryable by
-- a BI tool or analyst without any additional transformation.
--
-- It must be able to answer all four business questions:
--   1. What is total revenue per product category?
--   2. Who are the top 10 customers by lifetime value?
--   3. What is the average basket size (distinct items per order)?
--   4. Which products appear most frequently in orders?
--
-- You may implement this as a single aggregated table or split it into multiple
-- report models (rpt_revenue_by_category, rpt_top_customers, etc.).
-- Document your choice.
--
-- Input: {{ ref('fct_orders') }}, {{ ref('dim_customers') }}, {{ ref('dim_products') }}
--
-- Suggested columns for a category-level summary:
--   category                varchar
--   total_orders            integer
--   total_items_sold        integer
--   total_revenue_usd       decimal(10,2)
--   avg_order_value_usd     decimal(10,2)
--   pct_of_total_revenue    decimal(5,2)   -- share of total revenue (0–100)

{{ config(materialized='table') }}

-- Your SQL here:
