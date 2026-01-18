-- models/marts/fct_messages.sql

select
    m.message_id,
    c.channel_key,
    d.date_key,
    m.message_text,
    length(m.message_text) as message_length,
    m.views as view_count,
    m.forwards as forward_count,
    m.has_image
from {{ ref('stg_telegram_messages') }} m
left join {{ ref('dim_channels') }} c
    on m.channel_id = c.channel_id
left join {{ ref('dim_dates') }} d
    on date(m.message_date) = d.full_date
