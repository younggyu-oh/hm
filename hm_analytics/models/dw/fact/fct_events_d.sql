{{ config(
    materialized='table'
) }}
-- incrementally update on a daily bases in production environment
-- since it's an small size assignment, no partitition


SELECT CAST(DATE_TRUNC('day', event_time) AS TEXT) AS event_date_utc,
       CAST(event_time AS TIMESTAMP) AS event_time_utc,
       coalesce(user_id,'null') as user_id,
       coalesce(event_type,'null') as event_type,
       coalesce(transaction_category,'null') as transaction_category,
       CAST(miles_amount AS DOUBLE) AS miles_amount,
       coalesce(platform,'null') as platform,
       coalesce(utm_source,'null') as utm_source,
       coalesce(country,'null') as country,
       CURRENT_TIMESTAMP AS etl_at_utc,

  FROM {{ source('manual_loaded','raw_events_d') }}
-- WHERE dt = '{{ ds_nodash }}'  (partition pruning - 20250614)
