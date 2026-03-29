# 🖱️ AI Virtual Mouse: Next-Gen Computer Vision Interface

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.13-orange?logo=google&logoColor=white)](https://google.github.io/mediapipe/)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9.54-red)](https://pyautogui.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance Human-Computer Interaction (HCI) application that leverages **Computer Vision** and **Machine Learning** to control a computer cursor via intuitive hand gestures. This project eliminates the need for physical hardware by using a standard webcam to interpret the user's intent in real-time.

---

## 🎯 **Core Features**

- **Precision Tracking**: Sub-pixel accurate cursor control using the index finger tip.
- **Smart Gestures**: 
  - 👆 **Pinch to Click**: Thumb-index pinch for left-click operations.
  - ✌️ **Dual-Finger Scroll**: Vertical scrolling using index and middle finger tracking.
- **Motion Smoothing**: Implements a configurable smoothing algorithm to eliminate hand jitter.
- **Dynamic Calibration**: Active detection zone (80% frame ratio) for optimized screen mapping.
- **Real-time Performance**: Optimized for 60+ FPS processing on modern hardware.

---

## 🛠️ **System Architecture**

The system follows a modular pipeline to ensure low latency and high accuracy:

1. **Capture**: Frames are captured at 720p/1080p from the local webcam.
2. **Detection**: MediaPipe's BlazePalm model identifies 21 hand landmarks.
3. **Coordinate Mapping**: Translation of normalized hand coordinates to OS screen resolution.
4. **Action Interpretation**: Euclidean distance-based gesture recognition for clicking and scrolling.
5. **Execution**: System-level events triggered via PyAutoGUI.

### **Gesture Key**
| Gesture | OS Action | Visual Indicator |
| :--- | :--- | :--- |
| **Index finger pointing** | **Mouse Movement** | Green dot on index tip |
| **Thumb-index pinch** | **Left Click** | "CLICK!" overlay |
| **Index + Middle raised** | **Vertical Scroll** | "SCROLL UP/DOWN" overlay |

---

## 💻 **Tech Stack**

- **Language**: [Python 3.12+](https://python.org)
- **Vision Engine**: [OpenCV](https://opencv.org) (Image preprocessing and UI overlay)
- **ML Framework**: [MediaPipe](https://google.github.io/mediapipe/) (Hand landmark tracking)
- **System Controller**: [PyAutoGUI](https://pyautogui.readthedocs.io/) (OS-level mouse event injection)
- **Math**: [NumPy](https://numpy.org) (Coordinate smoothing and geometry)

---

## 🚀 **Quick Start**

### **1. Environment Setup**
It is highly recommended to use a virtual environment for the setup:
```bash
# Clone the repository
git clone https://github.com/ayushcodes13/gesture-controlled-virtual-mouse.git
cd gesture-controlled-virtual-mouse

# Create and Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### **2. Launch Application**
```bash
# Run the main application
python3 main.py
```

### **3. Interaction Guide**
- **Move Hand**: Keep your hand within the **Blue Rectangle** for tracking.
- **Toggle Control**: Press `'t'` to enable/disable mouse control safely.
- **Exit**: Press `'q'` to close the interface.

---

## 🔧 **Troubleshooting (macOS)**

> [!IMPORTANT]
> **Accessibility Permissions**: macOS requires explicit permission for `PyAutoGUI` to control the mouse.
> 1. Go to **System Settings** > **Privacy & Security**.
> 2. Click **Accessibility**.
> 3. Add and enable your **Terminal** or **IDE** (e.g., VS Code).

> [!TIP]
> **Webcam Not Opening?** Check if another app (Zoom, Teams) is using the camera. On Apple Silicon (M1/M2/M3), ensure you are using the ARM64 build of Python for maximum performance.

---

## 🎓 **Academic Project Note**
This project was developed as part of a **Computer Vision and HCI** curriculum. It demonstrates the application of real-time pose estimation and its integration with system-level APIs to create seamless human-machine interfaces.

## 🔮 **Future Scope**
- [ ] **Multi-Hand Support**: Separate gestures for left and right hands.
- [ ] **Voice Integration**: Voice-activated commands for desktop operations.
- [ ] **Low-Light Optimization**: Improved tracking using IR-capable webcams.
- [ ] **Custom Gesture Mapping**: Allow users to record and map their own gestures.

---

### **License**
Distributed under the MIT License. See `LICENSE` for more information.

---
**Developed by [Ayush Rout](https://github.com/ayushcodes13)**  
*College of Computer Science & Engineering*