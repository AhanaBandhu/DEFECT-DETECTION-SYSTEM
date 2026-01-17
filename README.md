# DEFECT-DETECTION-SYSTEM

The **Defect Detection System** is a real-time **client–server–based visual inspection application** developed using **Python, OpenCV, and Flask**. The system uses **HTTP video streaming** to collect live camera feeds from multiple client machines and display them on a centralized server dashboard.

A **Region of Interest (ROI)** is selected on the live video stream, and any visual changes such as cracks or surface defects within this region are detected and highlighted in real time. The system is designed to be robust against lighting variations and background noise, making it suitable for continuous monitoring where manual inspection is difficult.

---

## Features
- Client–server architecture using HTTP streaming  
- Live multi-camera feed monitoring  
- Manual ROI selection for focused inspection  
- Real-time defect and crack detection  
- Visual highlighting of detected defects  
- Noise and illumination variation filtering  

---

## Applications
- Infrastructure monitoring (bridges, tunnels, pipelines)  
- Crack detection in buildings and industrial surfaces  
- Monitoring museum artifacts and heritage structures  
- Surveillance in hazardous or inaccessible areas  

---

## Technologies Used
- **Frontend:** HTML, CSS  
- **Backend:** Flask (Python)  
- **Image Processing:** OpenCV, NumPy  
- **Networking:** HTTP-based video streaming  

---

## Setup and Installation
```bash
git clone https://github.com/AhanaBandhu/my-crack-detection-system.git
cd my-crack-detection-system
pip install flask opencv-python numpy
python app.py
```



<img src="https://github.com/user-attachments/assets/fa82e8cb-bee7-4cd1-a829-be3846e5e786" width="500">&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://github.com/user-attachments/assets/fea5c8ee-53d4-4352-8b46-db7ae608c1fa" width="120">&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://github.com/user-attachments/assets/c6b28165-250b-450f-8313-655602ae47a7" width="300">




