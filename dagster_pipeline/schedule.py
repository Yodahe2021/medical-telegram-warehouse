from dagster import ScheduleDefinition
from job import medical_telegram_pipeline

daily_medical_pipeline_schedule = ScheduleDefinition(
    job=medical_telegram_pipeline,
    cron_schedule="0 2 * * *"  # Runs daily at 02:00
)
