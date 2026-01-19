select
    d.detection_id,
    d.message_id,
    m.channel_key,
    d.object_class,
    d.confidence,
    d.confidence_level,
    d.created_at

from {{ ref('stg_image_detections') }} d
join {{ ref('fct_messages') }} m
  on d.message_id = m.message_id
SELECT
    detection_id,
    message_id,
    channel_username,

    object_class,

    CASE
        WHEN object_class = 'pharmaceutical' THEN 'Product'
        WHEN object_class = 'medical_device' THEN 'Equipment'
        WHEN object_class = 'cosmetics' THEN 'Cosmetics'
        ELSE 'Other'
    END AS content_type,

    confidence,
    image_path,
    created_at
FROM {{ ref('stg_image_detections') }}
