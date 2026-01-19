from dagster import op
import subprocess

@op(description="Run YOLOv8 image detection and store results")
def yolo_enrichment_op():
    subprocess.run(
        ["python", "src/enrichment/yolo_detect.py"],
        check=True
    )
