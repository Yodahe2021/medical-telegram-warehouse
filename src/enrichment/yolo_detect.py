MEDICAL_CLASSES = {
    "pill": "pharmaceutical",
    "tablet": "pharmaceutical",
    "capsule": "pharmaceutical",
    "syringe": "medical_device",
    "bandage": "medical_device",
    "cream": "cosmetics",
    "ointment": "cosmetics"
}

import os
from ultralytics import YOLO
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
model = YOLO("yolov8n.pt")

IMAGE_ROOT = "data/raw/images"

def run_detection():
    with engine.begin() as conn:
        for channel in os.listdir(IMAGE_ROOT):
            channel_path = os.path.join(IMAGE_ROOT, channel)

            if not os.path.isdir(channel_path):
                continue

            for img in os.listdir(channel_path):
                if not img.endswith(".jpg"):
                    continue

                message_id = int(img.replace(".jpg", ""))
                image_path = os.path.join(channel_path, img)

                results = model(image_path)

                for r in results:
                    for box in r.boxes:
                        cls = model.names[int(box.cls)]
                        conf = float(box.conf)

                        if conf < 0.5:
                            continue  # confidence threshold

                        conn.execute(
                            text("""
                                INSERT INTO image_detections
                                (message_id, channel_username, object_class, confidence, image_path)
                                VALUES (:message_id, :channel, :cls, :conf, :path)
                            """),
                            {
                                "message_id": message_id,
                                "channel": channel,
                                "cls": cls,
                                "conf": conf,
                                "path": image_path
                            }
                        )

    print("✅ Image enrichment completed")

if __name__ == "__main__":
    run_detection()
category = MEDICAL_CLASSES.get(det_class, "other")

conn.execute(
    text("""
        INSERT INTO image_detections (
            message_id,
            channel_username,
            object_class,
            confidence,
            image_path
        )
        VALUES (:message_id, :channel, :object_class, :confidence, :image_path)
    """),
    {
        "message_id": message_id,
        "channel": channel,
        "object_class": category,
        "confidence": float(conf),
        "image_path": image_path
    }
)
