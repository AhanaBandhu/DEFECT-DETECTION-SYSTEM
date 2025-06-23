import cv2
import os
import time
from datetime import datetime
from skimage.metrics import structural_similarity as ssim

SAVE_DIR = "static/captured_images"

def capture_image(camera, filename):
    if camera is None:
        print("ERROR: Camera not accessible.")
        return None

    ret, frame = camera.read()
    if ret:
        cv2.imwrite(filename, frame)
        return frame
    return None

def detect_cracks(reference, new_image):
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    (score, diff) = ssim(ref_gray, new_gray, full=True)
    diff = (diff * 255).astype("uint8")

    # Apply thresholding
    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]

    # Draw rectangles around cracks
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(new_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    processed_image_path = os.path.join(SAVE_DIR, "processed_latest.jpg")
    cv2.imwrite(processed_image_path, new_image)

def capture_reference_image():
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    # Define the path for the reference image
    reference_image_path = os.path.join(SAVE_DIR, "reference.jpg")
    
    # Open the camera
    camera = cv2.VideoCapture(0)
    time.sleep(2)  # Allow the camera to warm up

    # Capture and overwrite the reference image
    ref_image = capture_image(camera, reference_image_path)
    if ref_image is None:
        print("ERROR: Failed to capture reference image.")
        return None

    if ref_image is not None:
        print(f"Reference image saved at {reference_image_path}")
    else:
        print("Error: Failed to capture reference image.")
    
    # Release the camera
    camera.release()

    return ref_image

def process_images(duration, interval):
    ref_image_path = os.path.join(SAVE_DIR, "reference.jpg")
    ref_image = cv2.imread(ref_image_path)

    if ref_image is None:
        print("ERROR: Reference image not found.")
        return

    
    camera = cv2.VideoCapture(0)
    start_time = time.time()

    while time.time() - start_time < duration:
        new_image = capture_image(camera, os.path.join(SAVE_DIR, "latest.jpg"))
        if new_image is not None:
            detect_cracks(ref_image, new_image)

        time.sleep(interval)
    
    camera.release()