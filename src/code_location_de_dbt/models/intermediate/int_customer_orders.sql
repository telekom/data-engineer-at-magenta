-- Intermediate model: customer order aggregates
--
-- Aggregate order-level totals per customer. This feeds into dim_customers
-- for lifetime value calculations.
--
-- Input:  {{ ref('int_order_items') }}
--
-- Expected output (one row per customer):
--   user_id              integer
--   total_orders         integer    -- count of distinct order_id
--   total_items          integer    -- sum of quantity across all orders
--   total_revenue_usd    decimal(10,2)
--   avg_order_value_usd  decimal(10,2)
--   first_order_date     date
--   last_order_date      date

{{ config(materialized='view') }}

-- Your SQL here:
