-- Staging model: users
--
-- Source: {{ source('raw', 'raw_users') }}
--
-- Your goal: clean the raw user data and give columns business-friendly names.
--
-- Expected output columns:
--   user_id         integer   -- from: id
--   username        varchar   -- from: username
--   email           varchar   -- from: email
--   phone           varchar   -- from: phone
--   full_name       varchar   -- derived: firstname || ' ' || lastname
--   city            varchar   -- from: address_city
--   zipcode         varchar   -- from: address_zipcode
--   geo_lat         varchar   -- from: address_geo_lat  (keep as string or cast to float?)
--   geo_long        varchar   -- from: address_geo_long
--
-- Note: Not all columns from the raw table need to appear in staging.
-- Decide which ones are worth keeping for downstream models.

{{ config(materialized='view') }}

-- Your SQL here:
