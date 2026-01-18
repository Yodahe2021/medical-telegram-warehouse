-- models/staging/stg_telegram_messages.sql

with raw_messages as (
    select
        m.message_id,
        m.channel_id,
        m.message_date,
        m.message_text,
        m.views,
        m.forwards,
        m.has_media,
        c.channel_username
    from {{ source('raw', 'telegram_messages') }} m
    left join {{ ref('stg_telegram_channels') }} c
        on m.channel_id = c.channel_id
)

select
    message_id,
    channel_id,
    channel_username,
    message_date,
    message_text,
    length(message_text) as message_length,
    views as view_count,
    forwards as forward_count,
    has_media as has_image
from raw_messages
where message_text is not null
