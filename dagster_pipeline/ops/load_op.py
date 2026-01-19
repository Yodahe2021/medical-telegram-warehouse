from dagster import op
import subprocess

@op(description="Load raw Telegram messages into PostgreSQL")
def load_raw_messages_op():
    subprocess.run(
        ["python", "src/db/insert_messages.py"],
        check=True
    )
