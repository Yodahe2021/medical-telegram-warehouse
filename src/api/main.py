from schemas import SearchQuery, ImageDetection

@app.post("/search", response_model=list[ImageDetection])
def search_detections(query: SearchQuery):
    sql = """
        SELECT message_id, channel_username, object_class, confidence, image_path
        FROM fct_image_detections
        WHERE object_class ILIKE :keyword
    """

    params = {"keyword": f"%{query.keyword}%"}

    if query.channel:
        sql += " AND channel_username = :channel"
        params["channel"] = query.channel

    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).fetchall()

    return rows
from schemas import ChannelActivity

@app.get("/channels/activity", response_model=list[ChannelActivity])
def channel_activity():
    sql = """
        SELECT
            channel_username,
            COUNT(DISTINCT message_id) AS total_messages,
            COUNT(*) AS total_images,
            AVG(confidence) AS avg_confidence
        FROM fct_image_detections
        GROUP BY channel_username
        ORDER BY total_images DESC
    """

    with engine.connect() as conn:
        return conn.execute(text(sql)).fetchall()
from schemas import VisualContentReport

@app.get("/reports/visual-content", response_model=list[VisualContentReport])
def visual_content_report():
    sql = """
        SELECT
            object_class,
            COUNT(*) AS detection_count,
            AVG(confidence) AS avg_confidence
        FROM fct_image_detections
        GROUP BY object_class
        ORDER BY detection_count DESC
    """

    with engine.connect() as conn:
        return conn.execute(text(sql)).fetchall()
