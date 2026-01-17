import os
from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("TELEGRAM_PHONE")

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE)
    me = await client.get_me()
    print("Connected as:", me.username)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
