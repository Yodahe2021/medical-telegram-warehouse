from sqlalchemy import Column, Integer, BigInteger, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TelegramChannel(Base):
    __tablename__ = "telegram_channels"

    channel_id = Column(Integer, primary_key=True)
    channel_username = Column(Text, unique=True, nullable=False)
    created_at = Column(TIMESTAMP)

class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    message_id = Column(BigInteger, primary_key=True)
    channel_id = Column(Integer, ForeignKey("telegram_channels.channel_id"))
    message_date = Column(TIMESTAMP)
    message_text = Column(Text)
    views = Column(Integer)
    forwards = Column(Integer)
    has_media = Column(Boolean)
    created_at = Column(TIMESTAMP)

class TelegramImage(Base):
    __tablename__ = "telegram_images"

    image_id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger, ForeignKey("telegram_messages.message_id"))
    image_path = Column(Text)
    created_at = Column(TIMESTAMP)
