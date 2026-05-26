# Elecruisers-vision

The following Program is below pipeline:

Pipeline:
Camera Input
↓
Capture Frames
↓
Resize / Normalize
↓
Preprocessing
↓
Feature Extraction

cv2 in Python is used for this project. The primary camera (webcam) is used as the input device.

Each frame is processed as follows:

The frame is resized to 640 × 480
Gaussian Blur is applied for noise reduction
A normalization function is defined (optional preprocessing step)
Features are extracted using:
Grayscale conversion
Edge detection using cv2.Canny()

The start() method handles camera initialization and runs a continuous loop. The loop can be stopped by pressing 'q', which safely releases the camera and closes all OpenCV windows.

![Output Screenshot](./assets/output.png)