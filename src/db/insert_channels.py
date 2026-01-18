from database import get_db
from models import TelegramChannel

channels = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma"
]

db = get_db()

for ch in channels:
    exists = db.query(TelegramChannel).filter_by(channel_username=ch).first()
    if not exists:
        db.add(TelegramChannel(channel_username=ch))
        print(f"Inserted channel: {ch}")
    else:
        print(f"Channel already exists: {ch}")

db.commit()
db.close()
