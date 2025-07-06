# Illegal Parking Detection System

This project uses computer vision to detect vehicles that are parked outside their designated spots.

## Features
- Real-time detection using YOLOv8
- Custom defined parking zones
- Visual marking of violations
- License plate detection using EasyOCR
- Violations logged with timestamp and plate number in CSV
- Optional email alerts on violations
- Web-based dashboard to filter and review violations

## How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Add your parking spot config in `configs/parking_spots.json`
3. Download `yolov8n.pt` from [Ultralytics](https://github.com/ultralytics/ultralytics) and place in `models/`
4. Run the main detection script:
```bash
python main.py
```
5. To view logged violations via dashboard:
```bash
streamlit run dashboard.py
```

## Email Alerts (Optional)
To enable email alerts:
- Set `EMAIL_ENABLED = True` in `utils.py`
- Fill in your email credentials and SMTP server

## Notes
- Camera must capture the full parking area clearly
- Use high resolution for accurate license plate recognition
