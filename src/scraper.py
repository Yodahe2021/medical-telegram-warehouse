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

# Optional: Only scrape messages from this date
START_DATE = datetime(2020, 1, 1, tzinfo=timezone.utc)

# Limits to avoid too many downloads
MAX_MESSAGES = 100       # max messages per channel
MAX_IMAGES = 100          # max images per channel
MESSAGE_DELAY = 0.3      # seconds between messages

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

    async for message in client.iter_messages(channel):
        # Stop if reached max messages
        if msg_count >= MAX_MESSAGES:
            break

        # Skip old messages
        if message.date < START_DATE:
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

        # Download photo if it exists and limit images
        if hasattr(message.media, "photo") and img_count < MAX_IMAGES:
            try:
                img_folder = os.path.join(IMG_DIR, channel)
                os.makedirs(img_folder, exist_ok=True)
                img_path = os.path.join(img_folder, f"{message.id}.jpg")
                await message.download_media(img_path)
                msg_dict["image_path"] = img_path
                img_count += 1
            except Exception as e:
                print(f"[{channel}] Failed to download image {message.id}: {e}")

        all_messages.append(msg_dict)
        msg_count += 1

        # Delay to avoid Telegram throttling
        await asyncio.sleep(MESSAGE_DELAY)

    # Save messages to JSON
    today_str = datetime.now().strftime("%Y-%m-%d")
    json_folder = os.path.join(RAW_DIR, today_str)
    os.makedirs(json_folder, exist_ok=True)
    json_path = os.path.join(json_folder, f"{channel}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_messages, f, ensure_ascii=False, indent=4)

    # Logging
    log_file = os.path.join(LOG_DIR, "scrape.log")
    with open(log_file, "a") as log:
        log.write(f"{datetime.now().isoformat()} - Scraped {len(all_messages)} messages from {channel}\n")
    print(f"[{channel}] Finished scraping {len(all_messages)} messages, {img_count} images downloaded.")

# -------------------------
# MAIN FUNCTION
# -------------------------
async def main_all():
    # Windows event loop fix
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        for ch in channels:
            print(f"Scraping channel: {ch}")
            await scrape_channel(ch, client)

    print("Scraping completed!")

# Entry point
if __name__ == "__main__":
    asyncio.run(main_all())
