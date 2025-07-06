import cv2
import json
from shapely.geometry import Polygon, box
from ultralytics import YOLO
from utils import load_parking_spots, draw_spots, log_violation, recognize_plate, send_email

VIDEO_SOURCE = 0  # or 'video.mp4'
PARKING_CONFIG = 'configs/parking_spots.json'
MODEL_PATH = 'models/yolov8n.pt'

model = YOLO(MODEL_PATH)
spots = load_parking_spots(PARKING_CONFIG)

cap = cv2.VideoCapture(VIDEO_SOURCE)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    violations = []

    for det in results.boxes:
        cls = int(det.cls[0])
        if cls not in [2, 3, 5, 7]:  # car, motorcycle, bus, truck
            continue

        x1, y1, x2, y2 = map(int, det.xyxy[0])
        car_box = box(x1, y1, x2, y2)
        matched = False

        for sid, polygon in spots.items():
            poly = Polygon(polygon)
            iou = car_box.intersection(poly).area / car_box.area
            if iou > 0.85:
                matched = True
                break

        if not matched:
            violations.append(((x1, y1, x2, y2), det.conf[0].item()))

    for (x1, y1, x2, y2), conf in violations:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, f"Violation {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        plate_number = recognize_plate(frame[y1:y2, x1:x2])
        image_path = log_violation(frame, x1, y1, x2, y2, plate_number)
        send_email(plate_number, image_path)

    draw_spots(frame, spots)
    cv2.imshow("Illegal Parking Detection", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()