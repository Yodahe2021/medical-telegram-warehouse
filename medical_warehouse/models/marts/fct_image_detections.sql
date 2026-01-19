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
