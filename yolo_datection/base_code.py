import torch
import cv2
import numpy as np
from ultralytics import YOLO

# Load custom YOLOv11 model
model = YOLO('yolo11n.pt')

# Set up GStreamer pipeline
cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # x1, y1, x2, y2, conf, cls

    # Visualize detections
    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        label = f"Class: {int(cls)}, Confidence: {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Display the frame with detections
    cv2.imshow("YOLO Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
