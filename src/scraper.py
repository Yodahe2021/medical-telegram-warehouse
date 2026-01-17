import os
import json
from datetime import datetime, timezone
from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
import sys

# -------------------------
# CONFIGURATION
# -------------------------
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("TELEGRAM_PHONE")

RAW_DIR = "data/raw/telegram_messages"
IMG_DIR = "data/raw/images"
LOG_DIR = "logs"

# Only scrape messages from this date
START_DATE = datetime(2020, 1, 1, tzinfo=timezone.utc)

# Safety limits
MAX_MESSAGES = 100        # max messages per channel
MAX_IMAGES = 100          # max images per channel
MESSAGE_DELAY = 0.3       # seconds between messages

# Ensure directories exist
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Channels to scrape
channels = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma"
]

# -------------------------
# SCRAPER FUNCTION
# -------------------------
async def scrape_channel(channel, client):
    all_messages = []
    img_count = 0
    msg_count = 0

    async for message in client.iter_messages(
        channel,
        offset_date=START_DATE,
        reverse=True
    ):
        # Stop if reached message limit
        if msg_count >= MAX_MESSAGES:
            break

        msg_dict = {
            "message_id": message.id,
            "channel_name": channel,
            "message_date": message.date.isoformat(),
            "message_text": message.message or "",
            "views": message.views or 0,
            "forwards": message.forwards or 0,
            "has_media": bool(message.media),
            "image_path": None
        }

        # Download photo (limited)
        if message.photo and img_count < MAX_IMAGES:
            try:
                img_folder = os.path.join(IMG_DIR, channel)
                os.makedirs(img_folder, exist_ok=True)
                img_path = os.path.join(img_folder, f"{message.id}.jpg")
                await message.download_media(img_path)
                msg_dict["image_path"] = img_path
                img_count += 1
            except Exception as e:
                print(f"[{channel}] Image download failed ({message.id}): {e}")

        all_messages.append(msg_dict)
        msg_count += 1

        # Delay to avoid throttling
        await asyncio.sleep(MESSAGE_DELAY)

    # Save messages to JSON
    today = datetime.now().strftime("%Y-%m-%d")
    json_folder = os.path.join(RAW_DIR, today)
    os.makedirs(json_folder, exist_ok=True)

    json_path = os.path.join(json_folder, f"{channel}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_messages, f, ensure_ascii=False, indent=4)

    # Logging
    log_path = os.path.join(LOG_DIR, "scrape.log")
    with open(log_path, "a") as log:
        log.write(
            f"{datetime.now().isoformat()} | {channel} | "
            f"{msg_count} messages | {img_count} images\n"
        )

    print(f"[{channel}] Finished: {msg_count} messages, {img_count} images")

# -------------------------
# MAIN FUNCTION
# -------------------------
async def main_all():
    # Windows asyncio fix
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async with TelegramClient("session_name", API_ID, API_HASH) as client:
        for channel in channels:
            try:
                print(f"Scraping channel: {channel}")
                await scrape_channel(channel, client)
            except Exception as e:
                print(f"[ERROR] {channel}: {e}")

    print("✅ Scraping completed!")

# Entry point
if __name__ == "__main__":
    asyncio.run(main_all())
