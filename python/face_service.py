print("✅ face_service.py has started...")

import cv2
from flask import Flask, Response, jsonify
from pathlib import Path
from utils import detect_faces_bgr

app = Flask(__name__)

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'backend' / 'storage' / 'models' / 'trainer.yml'
LABEL_PATH = MODEL_PATH.with_suffix('.labels')

recognizer = None
label_to_name = {}

def load_model():
    global recognizer, label_to_name
    if not MODEL_PATH.exists():
        print("❌ Model file not found:", MODEL_PATH)
        return False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(MODEL_PATH))
    print("✅ Model loaded from", MODEL_PATH)

    label_to_name.clear()
    if LABEL_PATH.exists():
        lines = LABEL_PATH.read_text(encoding='utf-8').splitlines()
        for line in lines:
            idx, name = line.split(',', 1)
            label_to_name[int(idx)] = name

    return True

# Load model on startup if exists
load_model()

def open_camera():
    """Try to open webcam with fallbacks."""
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cam.isOpened():
        print("⚠️ Camera 0 failed, trying index 1...")
        cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cam.isOpened():
        raise RuntimeError("❌ Could not open any webcam")

    print("✅ Camera opened successfully")
    return cam

def gen_frames():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cam.isOpened():
        raise RuntimeError("❌ Could not open webcam")

    print("✅ Camera 0 opened (640x480)")

    try:
        while True:
            ok, frame = cam.read()
            if not ok or frame is None:
                print("⚠️ Failed to grab frame")
                continue

            # Just in case, resize to avoid issues
            frame = cv2.resize(frame, (640, 480))

            gray, faces, rois = detect_faces_bgr(frame)
            for (x, y, w, h), roi in zip(faces, rois):
                label_text = "Unknown"
                if recognizer is not None:
                    label, conf = recognizer.predict(roi)
                    label_text = f"{label_to_name.get(label, 'Unknown')} ({conf:.0f})"

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label_text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Encode JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("⚠️ JPEG encode failed")
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    finally:
        cam.release()
        print("✅ Camera released")


@app.get('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.get('/reload')
def reload_model():
    ok = load_model()
    return jsonify({"reloaded": ok})

@app.get('/health')
def health():
    return {"modelLoaded": recognizer is not None}

if __name__ == '__main__':
    print("flask is running")
    app.run(host='0.0.0.0', port=5000, debug=True)
