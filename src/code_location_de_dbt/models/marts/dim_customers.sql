-- Mart model: customer dimension
--
-- One row per customer, combining user profile with lifetime order statistics.
--
-- Input:  {{ ref('stg_users') }}
--         {{ ref('int_customer_orders') }}
--
-- Suggested columns:
--   user_id              integer   (PK)
--   username             varchar
--   email                varchar
--   full_name            varchar
--   city                 varchar
--   total_orders         integer
--   total_items          integer
--   total_revenue_usd    decimal(10,2)
--   avg_order_value_usd  decimal(10,2)
--   first_order_date     date
--   last_order_date      date

{{ config(materialized='table') }}

-- Your SQL here:
