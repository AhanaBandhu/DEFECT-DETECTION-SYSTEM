from flask import Flask, render_template, jsonify, Response
import requests

app = Flask(__name__)

# Example camera feeds (replace with your real camera client endpoints)
STREAM_URLS = [
    "http://10.100.254.194:5000",  # Camera 1
    "http://192.168.0.110:5000",     # Camera 2
    "http://127.0.0.1:5003",     # Camera 3
    "http://10.100.254.194:5000"      # Camera 4
]


@app.route("/")
def index():
    return render_template("index_03.html", streams=STREAM_URLS)


@app.route("/proxy/<int:cam_id>")
def proxy_stream(cam_id):
    """Proxy MJPEG stream from camera"""
    def generate():
        url = STREAM_URLS[cam_id]
        with requests.get(f"{url}/video", stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(generate(), content_type="multipart/x-mixed-replace; boundary=frame")


import traceback
import sys
import requests
from flask import jsonify

@app.route("/status")
def dashboard_status():
    camera_states = []
    for i, url in enumerate(STREAM_URLS):
        cam_state = {"active": False, "defect": False}
        try:
            r = requests.get(f"{url}/status", timeout=1)
            if r.status_code == 200:
                data = r.json()
                cam_state["active"] = bool(data.get("active", False))
                cam_state["defect"] = bool(data.get("defect", False))
                print(f"Camera {i}: {cam_state}", flush=True)
            else:
                print(f"Camera {i} returned status code {r.status_code}", flush=True)

        except Exception as e:
            # print safely even if Windows console encoding fails
            err_info = traceback.format_exc()
            try:
                sys.stdout.buffer.write(
                    f"Error fetching status from {url}: {err_info}\n".encode("utf-8", "ignore")
                )
            except Exception:
                pass  # completely ignore printing errors to prevent crash

        camera_states.append(cam_state)

    return jsonify(camera_states)




@app.route("/defect_images/<int:cam_id>")
def defect_images(cam_id):
    """Return links to camera server's images"""
    url = STREAM_URLS[cam_id]
    return jsonify({
        "initial": f"{url}/initial_image",
        "defect": f"{url}/defect_image"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)