{{ config(
    materialized='table'
) }}
-- incrementally update on a daily bases in production environment
-- since it's an small size assignment, no partitition

select
  d.month_start_date,
  d.month,
  coalesce(e.transaction_category, 'all') as transaction_category,
  coalesce(e.country, 'all')  as country,
  count(distinct e.user_id) as mau,
  replace(d.month_start_date, '-', '') as dt
from {{ ref('fct_events_d') }} e
     join {{ source('manual_loaded','dim_date') }} d
     on e.event_date_utc = d.base_date
group by
  d.month_start_date, d.month,
  grouping sets (
    (e.country),
    (e.transaction_category),
    (e.country, e.transaction_category),
    ()
  )
