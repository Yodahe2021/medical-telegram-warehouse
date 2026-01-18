import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# -------------------------
# LOAD ENV
# -------------------------
load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DB_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

DATA_DIR = "data/raw/telegram_messages/2026-01-17"

engine = create_engine(DB_URL)

# -------------------------
# MAIN INGEST FUNCTION
# -------------------------
def insert_images():
    with engine.begin() as conn:
        total_inserted = 0

        for file in os.listdir(DATA_DIR):
            if not file.endswith(".json"):
                continue

            channel_username = file.replace(".json", "")
            file_path = os.path.join(DATA_DIR, file)

            with open(file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)

            for msg in messages:
                if not msg.get("image_path"):
                    continue

                conn.execute(
                    text("""
                        INSERT INTO telegram_images (
                            message_id,
                            image_path
                        )
                        VALUES (
                            :message_id,
                            :image_path
                        )
                        ON CONFLICT DO NOTHING
                    """),
                    {
                        "message_id": msg["message_id"],
                        "image_path": msg["image_path"]
                    }
                )
                total_inserted += 1

        print(f"✅ Inserted {total_inserted} images")

# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    insert_images()
