from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("data/raw/images/CheMed123/25.jpg")

results[0].show()
