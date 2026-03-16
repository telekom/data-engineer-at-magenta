-- Staging model: products
--
-- Source: {{ source('raw', 'raw_products') }}
--
-- Your goal: clean and type the raw product data.
--
-- Expected output columns (rename as you see fit — document your choices):
--   product_id      integer       -- from: id
--   product_title   varchar       -- from: title
--   price_usd       decimal(10,2) -- from: price (cast from float)
--   category        varchar       -- from: category
--   description     varchar       -- from: description
--   image_url       varchar       -- from: image
--   rating_score    decimal(3,1)  -- from: rating_rate
--   rating_count    integer       -- from: rating_count
--
-- DECISION POINT: Naming conventions
--   How did you decide what to call columns?
--   Did you follow a project-wide convention (snake_case, _id suffix, etc.)?
--   Leave a comment explaining your approach.
--
-- # DECISION: I named columns by ...

{{ config(materialized='view') }}

-- Your SQL here:
