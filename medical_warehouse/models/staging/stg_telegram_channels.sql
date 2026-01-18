-- models/staging/stg_telegram_channels.sql

with raw_channels as (
    select
        channel_id,
        channel_username,
        created_at
    from {{ source('raw', 'telegram_channels') }}  -- matches schema.yml source
)

select
    channel_id,
    lower(channel_username) as channel_username,  -- standardize username
    created_at
from raw_channels
where channel_username is not null
