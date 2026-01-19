from dagster import job

from ops.scrape_op import scrape_telegram_op
from ops.load_op import load_raw_messages_op
from ops.dbt_op import run_dbt_models_op
from ops.yolo_op import yolo_enrichment_op


@job(description="End-to-end Medical Telegram Data Pipeline")
def medical_telegram_pipeline():
    scrape_telegram_op()
    load_raw_messages_op()
    run_dbt_models_op()
    yolo_enrichment_op()
