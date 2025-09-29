import cv2

# Load the default Haar Cascade for face detection
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def detect_faces_bgr(frame_bgr):
    """
    Converts the frame to grayscale and detects faces.
    Returns:
      - gray image
      - list of face bounding boxes
      - list of face ROI images (grayscale)
    """
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    rois = [gray[y:y+h, x:x+w] for (x, y, w, h) in faces]
    return gray, faces, rois
