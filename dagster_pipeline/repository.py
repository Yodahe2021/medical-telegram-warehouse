from dagster import repository
from job import medical_telegram_pipeline
from schedule import daily_medical_pipeline_schedule

@repository
def medical_telegram_repository():
    return [
        medical_telegram_pipeline,
        daily_medical_pipeline_schedule
    ]
