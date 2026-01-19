from dagster import op
import subprocess

@op(description="Run dbt transformations (staging + marts)")
def run_dbt_models_op():
    subprocess.run(
        ["dbt", "run"],
        cwd="medical_warehouse",
        shell=True,
        check=True
    )
