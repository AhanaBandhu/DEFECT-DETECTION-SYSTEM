# DEFECT-DETECTION-SYSTEM

The Defect Detection System is a real-time surveillance application that activates the camera upon clicking the start button and captures images at regular or user-defined intervals. It compares each new image with the previous one to detect any defects such as cracks or surface changes. If no difference is found, the old image is replaced; if a defect is detected, it is highlighted. The system filters out background noise and lighting variations, making it suitable for monitoring structures like bridges where human inspection is difficult.

## Features
* Live camera activation through the web interface
* Capture images at regular or user-defined time intervals
* Compare each new image with the previous one
* Detect and highlight cracks, defects, or visual changes
* Filter out lighting noise and background distractions

## APPLICATIONS 
* Useful for infrastructure monitoring (e.g., bridges, tunnels, pipelines) , cracks in museum artefacts and in places where human inspection is difficult

## TECHNOLOGIES USED
* Frontend - html,css
* Image Processing- Python (OpenCV ,scikit-image ,imutils ,NumPy ,time ,os)
* Backend - Flask

## Setup and Installation
* Clone the repository : git clone https://github.com/AhanaBandhu/my-crack-detection-system.git   cd my-crack-detection-system
* Install required packages: pip install flask opencv-python scikit-image imutils numpy
* Run the Flask app:python app.py

## How to Use
* Open the web app in your browser
* Click the "Start" button to begin live camera feed
* Set the image capture interval (in seconds)
* The app captures and compares images automatically
* If a defect is detected, it is highlighted on screen
* Click "Stop" to end the session

## Project Structure
* app.py: Main Flask application
* detection.py: Core crack/defect detection logic
* templates/: Contains HTML files
* index.html: Frontend interface
* static/: Contains static assets
* styles.css: Web styling

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a Pull Request.

## License
This project is licensed under the MIT License.









