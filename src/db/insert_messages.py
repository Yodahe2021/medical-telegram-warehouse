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
# HELPERS
# -------------------------
def get_channel_id(channel_username, conn):
    result = conn.execute(
        text("""
            SELECT channel_id 
            FROM telegram_channels 
            WHERE channel_username = :username
        """),
        {"username": channel_username}
    ).fetchone()

    return result[0] if result else None


# -------------------------
# MAIN INGEST FUNCTION
# -------------------------
def insert_messages():
    with engine.begin() as conn:
        for file in os.listdir(DATA_DIR):
            if not file.endswith(".json"):
                continue

            channel_username = file.replace(".json", "")
            channel_id = get_channel_id(channel_username, conn)

            if not channel_id:
                print(f"⚠ Channel not found in DB: {channel_username}")
                continue

            file_path = os.path.join(DATA_DIR, file)
            with open(file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)

            inserted = 0

            for msg in messages:
                conn.execute(
                    text("""
                        INSERT INTO telegram_messages (
                            message_id,
                            channel_id,
                            message_date,
                            message_text,
                            views,
                            forwards,
                            has_media
                        )
                        VALUES (
                            :message_id,
                            :channel_id,
                            :message_date,
                            :message_text,
                            :views,
                            :forwards,
                            :has_media
                        )
                        ON CONFLICT (message_id) DO NOTHING
                    """),
                    {
                        "message_id": msg["message_id"],
                        "channel_id": channel_id,
                        "message_date": msg["message_date"],
                        "message_text": msg["message_text"],
                        "views": msg["views"],
                        "forwards": msg["forwards"],
                        "has_media": msg["has_media"]
                    }
                )
                inserted += 1

            print(f"✅ {channel_username}: processed {inserted} messages")


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    insert_messages()
