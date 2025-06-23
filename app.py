import os
import time
from flask import Flask, render_template, request, jsonify
from crack_detector import capture_reference_image, process_images

app = Flask(_name_)

# Image folder paths
IMAGE_FOLDER = "static/captured_images"
REFERENCE_IMAGE = os.path.join(IMAGE_FOLDER, "reference.jpg")
PROCESSED_IMAGE = os.path.join(IMAGE_FOLDER, "processed_latest.jpg")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_detection():
    data = request.json
    duration = int(data.get('duration', 10))
    interval = int(data.get('interval', 2))

    # Validate user input
    if duration <= 0 or interval <= 0:
        return jsonify({'error': 'Duration and interval must be positive integers'}), 400

    print("DEBUG: Start button clicked - Duration:", duration, "Interval:", interval)

    # Capture reference image
    reference_image = capture_reference_image()
    if reference_image is None:
        print("ERROR: Failed to capture reference image!")
        return jsonify({'error': 'Failed to capture reference image'}), 500

    print("DEBUG: Reference image captured successfully!")

    # Start processing images in the background
    process_images(duration, interval)

    return jsonify({
        'message': 'Processing started',
        'reference_image': f"/{REFERENCE_IMAGE}",
        'processed_image': f"/{PROCESSED_IMAGE}"
    }), 200

if _name_ == '_main_':
    app.run(debug=True)