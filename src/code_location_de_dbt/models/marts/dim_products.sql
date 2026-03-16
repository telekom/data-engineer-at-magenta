-- Mart model: product dimension
--
-- One row per product with current catalog attributes.
--
-- Input: {{ ref('stg_products') }}
--
-- Suggested columns:
--   product_id       integer   (PK)
--   product_title    varchar
--   category         varchar
--   price_usd        decimal(10,2)
--   rating_score     decimal(3,1)
--   rating_count     integer
--   image_url        varchar

{{ config(materialized='table') }}

-- Your SQL here:
