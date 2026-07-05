# 🦾 Gesture-Controlled Virtual Mouse

A real-time, computer vision-based virtual mouse that allows you to control your computer's cursor, clicks, and scrolling using hand gestures. Built with Python, this project leverages Google's MediaPipe for robust 3D hand-landmark tracking and PyAutoGUI for operating system integration.

## ✨ Features

* **Zero-Touch Navigation:** Control your OS entirely through your webcam.
* **Precise Cursor Tracking:** Maps index finger spatial coordinates to screen resolution using linear interpolation and low-pass filtering for smooth, jitter-free movement.
* **Intuitive Gestures:**
  * ☝️ **Move Cursor:** Raise your Index Finger.
  * 🤏 **Left Click:** Pinch your Index Finger and Thumb together.
  * ✌️ **Scroll Down:** Raise both Index and Middle fingers together.
* **Dynamic Visual Feedback:** Displays real-time skeletal tracking and an active tracking bounding box on the camera feed.

## 🛠️ Tech Stack

* **Python 3.x**
* **OpenCV (`cv2`):** Hardware interfacing and image preprocessing.
* **MediaPipe:** Machine learning pipeline for hand landmark detection.
* **PyAutoGUI:** OS-level execution for mouse events.
* **NumPy & Math:** Spatial reasoning, distance calculation, and coordinate mapping.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/virtual-mouse.git](https://github.com/yourusername/virtual-mouse.git)
   cd virtual-mouse
