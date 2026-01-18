-- models/marts/dim_channels.sql

with channels as (
    select
        channel_id,
        channel_username,
        created_at,
        -- You can classify channel_type manually or with logic
        case 
            when lower(channel_username) like '%pharma%' then 'Pharmaceutical'
            when lower(channel_username) like '%cosmetic%' then 'Cosmetics'
            else 'Medical'
        end as channel_type
    from {{ ref('stg_telegram_channels') }}
)

select
    row_number() over () as channel_key,  -- surrogate key
    channel_id,
    channel_username,
    channel_type,
    min(created_at) over () as first_post_date,
    max(created_at) over () as last_post_date
from channels
