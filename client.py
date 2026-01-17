from flask import Flask, Response, send_file, jsonify
import cv2
import numpy as np
import os
import time
from glob import glob

# ---------- Configuration ----------
CAM_ID = 0  # unique per camera
app = Flask(__name__)
cap = cv2.VideoCapture(CAM_ID)

roi = None
reference_lab = None
change_detected = False
latest_defect_path = None  # track latest file

# ---------- Paths ----------
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

INITIAL_IMAGE_PATH = os.path.join(STATIC_FOLDER, f"initial_{CAM_ID}.jpg")


# ---------- ROI Selection ----------
def initialize_roi():
    global roi, reference_lab
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Cannot read from camera.")
        exit()

    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")

    x, y, w, h = roi
    if w == 0 or h == 0:
        print("❌ Invalid ROI selected.")
        exit()

    roi_img = frame[y:y + h, x:x + w]
    reference_lab = cv2.cvtColor(roi_img, cv2.COLOR_BGR2LAB)
    reference_lab = cv2.GaussianBlur(reference_lab, (7, 7), 0)

    cv2.imwrite(INITIAL_IMAGE_PATH, roi_img)
    print(f"[CAM {CAM_ID}] ✅ Initial ROI saved → {INITIAL_IMAGE_PATH}")


# ---------- Frame Processing ----------
def process_frame(frame):
    global roi, reference_lab, change_detected, latest_defect_path

    if roi is None or reference_lab is None:
        return frame

    x, y, w, h = roi
    current_roi = frame[y:y + h, x:x + w]
    current_lab = cv2.cvtColor(current_roi, cv2.COLOR_BGR2LAB)
    blurred = cv2.GaussianBlur(current_lab, (7, 7), 0)

    diff = cv2.absdiff(reference_lab[:, :, 1:], blurred[:, :, 1:])
    mag = cv2.sqrt(diff[:, :, 0].astype(np.float32)**2 + diff[:, :, 1].astype(np.float32)**2)
    mag = np.uint8(mag)

    _, thresh = cv2.threshold(mag, 5, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    change_detected = any(cv2.contourArea(cnt) > 300 for cnt in contours)

    if change_detected:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        latest_defect_path = os.path.join(STATIC_FOLDER, f"defect_{CAM_ID}_.jpg")
        cv2.imwrite(latest_defect_path, current_roi)
        print(f"[CAM {CAM_ID}] ⚠️ Defect saved → {latest_defect_path}")

    for cnt in contours:
        if cv2.contourArea(cnt) > 300:
            cx, cy, cw, ch = cv2.boundingRect(cnt)
            cv2.rectangle(current_roi, (cx, cy), (cx + cw, cy + ch), (0, 0, 255), 2)

    frame[y:y + h, x:x + w] = current_roi
    return frame


# ---------- Stream ----------
def generate_stream():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        processed = process_frame(frame)
        _, jpeg = cv2.imencode(".jpg", processed)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")


@app.route("/video")
def video_feed():
    return Response(generate_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


# ---------- API ----------
@app.route("/status")
def status():
    return jsonify({
        "active": cap.isOpened(),
        "defect": change_detected,
        "latest_defect": os.path.basename(latest_defect_path) if latest_defect_path else None,
        "timestamp": int(time.time())
    })


@app.route("/initial_image")
def initial_image():
    if os.path.exists(INITIAL_IMAGE_PATH):
        return send_file(INITIAL_IMAGE_PATH, mimetype="image/jpeg", max_age=0)
    return ("", 404)


@app.route("/defect_image")
def defect_image():
    """Serve the latest defect image for popup."""
    global latest_defect_path

    if latest_defect_path and os.path.exists(latest_defect_path):
        return send_file(latest_defect_path, mimetype="image/jpeg", max_age=0)

    # fallback: get most recent saved file
    defect_files = sorted(glob(os.path.join(STATIC_FOLDER, f"defect_{CAM_ID}_*.jpg")), reverse=True)
    if defect_files:
        latest_defect_path = defect_files[0]
        return send_file(latest_defect_path, mimetype="image/jpeg", max_age=0)

    return ("", 404)


# ---------- Run ----------
if __name__ == "__main__":
    initialize_roi()
    print(f"[CAM {CAM_ID}] Streaming → http://localhost:{5000 + CAM_ID}")
    app.run(host="0.0.0.0", port=5000 + CAM_ID, debug=False)