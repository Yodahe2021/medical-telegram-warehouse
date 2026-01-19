with source as (

    select
        detection_id,
        message_id,
        channel_username,
        lower(object_class) as object_class,
        confidence,
        image_path,
        created_at

    from {{ source('raw', 'image_detections') }}

),

cleaned as (

    select
        detection_id,
        message_id,
        channel_username,
        object_class,
        confidence,
        image_path,
        created_at,

        -- Categorize confidence
        case
            when confidence >= 0.80 then 'high'
            when confidence >= 0.50 then 'medium'
            else 'low'
        end as confidence_level

    from source
    where confidence >= 0.50   -- filter weak detections
)

select * from cleaned
