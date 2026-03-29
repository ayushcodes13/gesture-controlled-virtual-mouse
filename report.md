# Project Report: Gesture Controlled Virtual Mouse using Computer Vision

---

## Abstract

This project presents the design and implementation of a **Gesture Controlled Virtual Mouse**, a software-based system that enables human-computer interaction through hand movements captured via a standard webcam. By leveraging Computer Vision and Deep Learning frameworks, specifically **OpenCV** and **MediaPipe**, the system eliminates the need for physical hardware like a mouse or trackpad. 

The primary objective was to create a responsive, real-time interface where specific hand landmarks are tracked to control cursor movement, left clicks, right clicks, and scrolling. The implementation utilizes a mapping algorithm to translate webcam coordinates to screen coordinates, incorporating smoothing techniques to mitigate cursor jitter. The final system achieves a high degree of accuracy in controlled lighting environments, offering a viable touchless alternative for modern computing tasks.

---

## 1. Introduction

The evolution of **Human-Computer Interaction (HCI)** has moved from punch cards and command-line interfaces to graphical user interfaces (GUI) dominated by the mouse and keyboard. While the traditional optical mouse has been the standard for decades, it remains tethered to physical surfaces and requires direct contact. In the modern era, there is a growing demand for more natural and intuitive ways to interact with digital systems. 

**Touchless interaction** is becoming a practical necessity due to the rise of ubiquitous computing and the need for sterile or hands-free environments. Computer Vision provides the perfect bridge for this transition. By using a simple camera as a sensor, we can interpret human gestures as intentional commands. This project focuses on developing a "Virtual Mouse" that uses hand tracking to perform all standard mouse operations. By identifying specific landmarks on the human hand, such as the tip of the index finger for movement and the pinch gesture for clicking, we create a seamless bridge between physical movement and digital execution.

---

## 2. Problem Statement

Traditional input devices face several limitations in specialized contexts. In medical environments, such as operating theaters, surgeons often need to interact with imaging software but cannot touch physical peripherals due to sterilization protocols. Similarly, for individuals with certain motor impairments, gripping a physical mouse can be difficult or impossible. 

The core problem addressed here is the lack of a low-cost, hardware-independent method for desktop navigation. There is a need for a system that can reliably interpret human intent through visual data in real time, overcoming common vision challenges like varying light, background noise, and hand tremors. Developing such a system requires balancing computational efficiency with tracking precision to ensure that the user does not feel a lag between their gesture and the system's response.

---

## 3. Objectives

The primary goals of this project are:
* To develop a **real-time hand tracking system** using a standard integrated or USB webcam.
* To implement precise cursor control by mapping hand landmarks to screen resolution coordinates.
* To design and integrate **gesture recognition** for essential mouse functions: single click, double click, and vertical scrolling.
* To apply mathematical smoothing filters to reduce the jitter caused by camera noise or slight hand tremors.
* To ensure the software is lightweight enough to run on standard consumer-grade laptops without significant CPU overhead.

---

## 4. Methodology

The system follows a sequential pipeline to transform raw video data into OS-level mouse events. 

### Step 1: Video Capture
Using the **OpenCV** library, frames are retrieved from the webcam at a consistent frame rate. Since MediaPipe performs better on RGB images, each captured frame is converted from BGR (the OpenCV default) to RGB.

### Step 2: Hand Detection and Landmark Extraction
The frame is passed through the **MediaPipe Hands** model. This model identifies 21 unique 3D landmarks on the hand. For cursor movement, we specifically track the **Index Finger Tip (Landmark 8)**.

### Step 3: Coordinate Mapping
To make the movement intuitive, the camera feed is horizontally flipped. The coordinates of the index finger are then normalized and scaled to match the user’s screen resolution. We define a "virtual boundary" within the frame to allow the user to reach the edges of the screen without overextending their arm.

### Step 4: Gesture Logic
Gesture recognition is based on the **Euclidean distance** between specific landmarks. 
* **Clicking:** Detected when the distance between the index finger tip and the thumb tip falls below a specific threshold.
* **Scrolling:** Triggered when both the index and middle fingers are raised and moved vertically.

---

## 5. Tools and Technologies

| Tool | Purpose |
| :--- | :--- |
| **Python** | The primary programming language used for logic and integration. |
| **OpenCV** | Used for capturing video, image preprocessing, and visual feedback. |
| **MediaPipe** | A high-fidelity framework by Google for hand landmark detection. |
| **PyAutoGUI** | The library used to programmatically control mouse movements and clicks. |
| **NumPy** | Used for mathematical operations and coordinate calculations. |

---

## 6. System Architecture

The architecture is structured as a continuous loop:

1.  **Input:** The webcam captures a raw image frame.
2.  **Preprocessing:** The image is flipped and converted to RGB color space.
3.  **Landmark Detection:** MediaPipe processes the image to locate 21 hand joints.
4.  **Coordinate Transformation:** Landmark coordinates are converted to screen pixel values $(x, y)$.
5.  **Smoothing Filter:** A weighted average is applied to prevent the cursor from shaking.
6.  **Event Execution:** PyAutoGUI executes the mouse move, click, or scroll event on the OS.

---

## 7. Implementation Details

### Cursor Smoothing Technique
One of the biggest challenges was hand tremor. To solve this, I implemented a **Linear Interpolation (Lerp)** approach. Instead of the cursor jumping directly to the new coordinates, it moves a fraction of the distance:

$$P_{new} = (1 - \alpha) \cdot P_{old} + \alpha \cdot P_{current}$$

Where $\alpha$ (the smoothing factor) was tuned to approximately **0.5**. This makes the cursor feel "heavy" yet smooth, much like a physical trackpad.

### Click Detection Logic
Initially, I used the distance between the index and middle finger for clicking, but it caused accidental clicks while moving the mouse. I switched to a **Thumb-Index Pinch**. This is more intentional and mimics the physical sensation of clicking.

> **Note:** A distance threshold of **30 pixels** (relative to frame size) was found to be the sweet spot for detecting a click without requiring the fingers to perfectly touch.

---

## 8. Challenges Faced and Solutions

* **Cursor Jitter:** Minor fluctuations in detection made it hard to click small icons. 
    * *Solution:* Implemented the smoothing algorithm mentioned above and added a "deadzone" where the cursor ignores movements smaller than 2 pixels.
* **Lighting Conditions:** In low-light dorm rooms, the landmarks would flicker.
    * *Solution:* Added a brightness normalization step and advised testing in well-lit environments.
* **Screen Reachability:** Moving the hand across the entire camera view was tiring.
    * *Solution:* I mapped a smaller 400x300 rectangle in the center of the camera feed to the full 1920x1080 screen resolution.

---

## 9. Results and Observations

The system was tested on a standard laptop with an i5 processor and 8GB RAM. 
* **Responsiveness:** The system maintains 25 to 30 FPS, providing a near-instant response.
* **Accuracy:** Movement is highly accurate, though clicking still has a slight learning curve for new users.
* **Usability:** It works best for browsing and light productivity. However, for tasks requiring high precision like graphic design, a physical mouse is still superior.

---

## 10. Applications

* **Medical:** Surgeons can navigate patient charts without touching a mouse.
* **Public Kiosks:** Reduces the spread of germs on public touchscreens.
* **Home Automation:** Controlling media players or smart TVs from a distance.

---

## 11. Limitations

* **Environmental Factors:** Requires consistent lighting and a relatively clean background.
* **Hardware Demand:** While lightweight, running a 720p stream with hand detection for hours can drain laptop batteries.
* **Physical Fatigue:** Holding one's arm in the air for long periods (known as "Gorilla Arm" syndrome) is the primary ergonomic limitation.

---

## 12. Future Scope

The next iteration of this project could involve:
* **Multi-Hand Support:** Using two hands for zooming in and out or rotating 3D models.
* **Voice Integration:** Combining gestures with voice commands for a "Multimodal" experience.
* **Customization:** A GUI where users can record their own gestures and map them to specific keyboard shortcuts.

---

## 13. Conclusion

Building the **Gesture Controlled Virtual Mouse** provided significant insights into the practicalities of Computer Vision. While the theory of landmark detection is straightforward, the real challenge lies in the "Human" part of HCI: handling tremors, ensuring ergonomic comfort, and making the software feel intuitive. 

This project successfully met its objectives, creating a functional, real-time alternative to physical input devices. It highlights a future where our interaction with machines is limited only by our movement, not by the hardware we hold.

---
