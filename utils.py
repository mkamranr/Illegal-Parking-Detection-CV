import json
import cv2
import os
import numpy as np
from datetime import datetime
import easyocr
import csv
import smtplib
from email.message import EmailMessage

reader = easyocr.Reader(['en'], gpu=False)

LOG_PATH = "logs/violations.csv"
EMAIL_ENABLED = False  # Set to True and configure below to enable emails
EMAIL_SENDER = "you@example.com"
EMAIL_RECEIVER = "admin@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
EMAIL_PASSWORD = "yourpassword"

def load_parking_spots(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def draw_spots(frame, spots):
    for sid, points in spots.items():
        pts = [tuple(pt) for pt in points]
        cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 2)
        cv2.putText(frame, sid, pts[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

def log_violation(frame, x1, y1, x2, y2, plate_number="Unknown"):
    os.makedirs("violations", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    crop = frame[y1:y2, x1:x2]
    filename = f"violations/violation_{timestamp}_{plate_number}.jpg"
    cv2.imwrite(filename, crop)

    # log to CSV
    with open(LOG_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, plate_number, filename])
    return filename

def recognize_plate(plate_region):
    results = reader.readtext(plate_region)
    if results:
        return results[0][1].replace(" ", "")
    return "Unknown"

def send_email(plate_number, image_path):
    if not EMAIL_ENABLED:
        return
    msg = EmailMessage()
    msg['Subject'] = f"Illegal Parking Violation Detected - Plate: {plate_number}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f"A vehicle with plate {plate_number} violated parking rules. See attached image.")
    with open(image_path, 'rb') as img:
        msg.add_attachment(img.read(), maintype='image', subtype='jpeg', filename=os.path.basename(image_path))
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)