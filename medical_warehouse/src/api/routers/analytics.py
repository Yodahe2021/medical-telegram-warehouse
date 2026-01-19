from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.api.database import get_db

router = APIRouter()

@router.get("/top-detected-products")
def top_detected_products(limit: int = 10, db: Session = Depends(get_db)):
    query = text("""
        SELECT object_class, COUNT(*) AS total_detections
        FROM image_detections
        GROUP BY object_class
        ORDER BY total_detections DESC
        LIMIT :limit
    """)
    result = db.execute(query, {"limit": limit}).fetchall()

    return [
        {"product": r[0], "detections": r[1]}
        for r in result
    ]

@router.get("/channel-image-activity")
def channel_image_activity(db: Session = Depends(get_db)):
    query = text("""
        SELECT channel_username, COUNT(*) AS images
        FROM image_detections
        GROUP BY channel_username
        ORDER BY images DESC
    """)
    result = db.execute(query).fetchall()

    return [
        {"channel": r[0], "image_count": r[1]}
        for r in result
    ]
@router.get("/channel-image-activity")
def channel_image_activity(db: Session = Depends(get_db)):
    query = text("""
        SELECT channel_username, COUNT(*) AS images
        FROM image_detections
        GROUP BY channel_username
        ORDER BY images DESC
    """)
    result = db.execute(query).fetchall()

    return [
        {"channel": r[0], "image_count": r[1]}
        for r in result
    ]
