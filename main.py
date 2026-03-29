#!/usr/bin/env python3
"""
AI Virtual Mouse - Computer Vision Based Mouse Control
This project uses OpenCV, MediaPipe, and PyAutoGUI to control mouse cursor
using hand gestures captured from webcam.
"""

import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
from typing import Tuple, List, Dict

class VirtualMouse:
    """
    AI Virtual Mouse: Real-time hand tracking and gesture recognition.
    
    This class handles the end-to-end pipeline of capturing frames from a webcam,
    detecting hand landmarks using MediaPipe, mapping coordinates to the screen,
    and executing system-level mouse events (movement, clicks, scrolling).
    """

    def __init__(self):
        # --- MediaPipe Configuration ---
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Higher detection confidence reduces false tracking
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # --- System & Mouse Settings ---
        pyautogui.FAILSAFE = False  # Allows moving mouse to screen corners
        self.screen_width, self.screen_height = pyautogui.size()

        # Movement Smoothing (0.0 to 1.0)
        # Lower values = more smoothing, but more latency
        self.smoothing_factor = 0.4
        self.prev_x, self.prev_y = 0, 0

        # --- Gesture Parameters ---
        # Click: Distance between THUMB_TIP (4) and INDEX_FINGER_TIP (8)
        self.click_distance_threshold = 0.05
        self.click_cooldown = 0.3  # Buffer to prevent double clicks
        self.last_click_time = 0

        # Scroll: Determined by height of INDEX and MIDDLE fingers
        self.scroll_finger_threshold = 0.8
        self.scroll_speed = 5

        # --- Camera & Tracking Calibration ---
        self.camera_width = 640
        self.camera_height = 480
        # Only use the center 80% of the frame to map to the full screen
        self.detection_region_ratio = 0.8

        # --- Runtime State ---
        self.mouse_control_enabled = True
        self.toggle_key = ord('t')  # Toggle logic control
        self.prev_frame_time = 0
        self.fps = 0


    def map_coordinates(self, x: float, y: float,
                       frame_width: int, frame_height: int) -> Tuple[int, int]:
        """
        Map hand coordinates from camera frame to screen coordinates
        """
        # Calculate the detection region (center 80% of frame)
        region_width = int(frame_width * self.detection_region_ratio)
        region_height = int(frame_height * self.detection_region_ratio)
        region_x = (frame_width - region_width) // 2
        region_y = (frame_height - region_height) // 2

        # Convert normalized coordinates to frame coordinates within region
        x_frame = int(x * frame_width)
        y_frame = int(y * frame_height)

        # Translate to region coordinates
        x_region = x_frame - region_x
        y_region = y_frame - region_y

        # Clamp to region bounds
        x_region = max(0, min(x_region, region_width))
        y_region = max(0, min(y_region, region_height))

        # Map region coordinates to screen coordinates
        screen_x = int(x_region * self.screen_width / region_width)
        screen_y = int(y_region * self.screen_height / region_height)

        return screen_x, screen_y

    def smooth_mouse_move(self, target_x: int, target_y: int) -> Tuple[int, int]:
        """
        Apply smoothing to mouse movement to reduce jitter
        """
        smoothed_x = int(self.prev_x + (target_x - self.prev_x) * self.smoothing_factor)
        smoothed_y = int(self.prev_y + (target_y - self.prev_y) * self.smoothing_factor)

        self.prev_x, self.prev_y = smoothed_x, smoothed_y
        return smoothed_x, smoothed_y

    def calculate_distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """
        Calculate distance between two points
        """
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def check_pinch_gesture(self, landmarks: List[Dict]) -> bool:
        """
        Detect pinch gesture (thumb and index finger touching)
        """
        thumb_tip = (landmarks[4]['x'], landmarks[4]['y'])
        index_tip = (landmarks[8]['x'], landmarks[8]['y'])

        distance = self.calculate_distance(thumb_tip, index_tip)
        return distance < self.click_distance_threshold

    def check_scroll_gesture(self, landmarks: List[Dict]) -> str:
        """
        Detect scroll gesture (two fingers up)
        Returns 'up', 'down', or None
        """
        # Get finger positions
        index_tip = landmarks[8]['y']
        middle_tip = landmarks[12]['y']

        # Check if both fingers are high (relatively low y values)
        if index_tip < self.scroll_finger_threshold and middle_tip < self.scroll_finger_threshold:

            # Determine scroll direction based on finger vertical movement
            middle_pip = landmarks[10]['y']  # Middle finger PIP joint

            # Scroll up if fingers are higher, down if lower
            avg_y = (index_tip + middle_tip) / 2
            if avg_y < 0.5:
                return 'up'
            else:
                return 'down'

        return None

    def fingers_up(self, landmarks: List[Dict]) -> int:
        """
        Count how many fingers are extended
        """
        fingers = []

        # Thumb check
        if landmarks[4]['x'] < landmarks[3]['x']:  # Thumb is extended
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers check
        for i in range(1, 5):
            if landmarks[4 + i * 4]['y'] < landmarks[2 + i * 4]['y']:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def draw_calibration_box(self, frame: np.ndarray) -> None:
        """
        Draw calibration/tracking region on frame
        """
        height, width = frame.shape[:2]
        region_width = int(width * self.detection_region_ratio)
        region_height = int(height * self.detection_region_ratio)
        region_x = (width - region_width) // 2
        region_y = (height - region_height) // 2

        cv2.rectangle(frame, (region_x, region_y),
                     (region_x + region_width, region_y + region_height),
                     (255, 0, 0), 2)

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a single frame from webcam
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        # Draw calibration box
        self.draw_calibration_box(frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Get all landmarks
            landmarks = []
            for i, landmark in enumerate(hand_landmarks.landmark):
                landmarks.append({
                    'id': i,
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })

            # Draw hand landmarks
            self.mp_drawing.draw_landmarks(
                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style())

            if self.mouse_control_enabled:
                # Get index finger tip position
                index_x = landmarks[8]['x']
                index_y = landmarks[8]['y']

                # Map to screen coordinates
                screen_x, screen_y = self.map_coordinates(index_x, index_y,
                                                       frame.shape[1], frame.shape[0])

                # Smooth the movement
                screen_x, screen_y = self.smooth_mouse_move(screen_x, screen_y)

                # Move mouse
                try:
                    pyautogui.moveTo(screen_x, screen_y)
                except pyautogui.FailSafeException:
                    pass
                except Exception as e:
                    print(f"Mouse move error: {e}")

                # Highlight index finger
                h, w = frame.shape[:2]
                index_x_px = int(index_x * w)
                index_y_px = int(index_y * h)
                cv2.circle(frame, (index_x_px, index_y_px), 8, (0, 255, 0), -1)

                # Check for click gesture
                current_time = time.time()
                if self.check_pinch_gesture(landmarks) and (current_time - self.last_click_time) > self.click_cooldown:
                    try:
                        pyautogui.click()
                        self.last_click_time = current_time
                        cv2.putText(frame, "CLICK!", (10, 200),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    except Exception as e:
                        print(f"Click error: {e}")

                # Check for scroll gesture
                scroll_direction = self.check_scroll_gesture(landmarks)
                if scroll_direction == 'up':
                    pyautogui.scroll(self.scroll_speed)
                    cv2.putText(frame, "SCROLL UP", (10, 240),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                elif scroll_direction == 'down':
                    pyautogui.scroll(-self.scroll_speed)
                    cv2.putText(frame, "SCROLL DOWN", (10, 240),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        return frame

    def display_status(self, frame: np.ndarray) -> None:
        """
        Display status information on frame
        """
        # Calculate FPS
        current_frame_time = time.time()
        if self.prev_frame_time != 0:
            self.fps = 1 / (current_frame_time - self.prev_frame_time)
        self.prev_frame_time = current_frame_time

        # Display status
        status_text = "ON" if self.mouse_control_enabled else "OFF"
        color = (0, 255, 0) if self.mouse_control_enabled else (0, 0, 255)

        cv2.putText(frame, f"Mouse Control: {status_text}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"FPS: {int(self.fps)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Display instructions
        cv2.putText(frame, "Press 't' to toggle mouse control", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, "Press 'q' to quit", (10, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Display hand landmarks key
        cv2.putText(frame, "Green: Index finger", (10, 130),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, "Red: Click zone (pinch)", (10, 145),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    def run(self):
        """
        Main function to start the virtual mouse
        """
        print("=== AI Virtual Mouse Starting ===")
        print("Controls:")
        print("- 't': Toggle mouse control on/off")
        print("- 'q': Quit application")
        print("\nEnsure your hand is clearly visible and face the camera.")

        # Initialize camera
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)

        if not cap.isOpened():
            print("Error: Could not open webcam")
            return

        print("Camera initialized successfully!")
        print("Move your hand within the blue rectangle...")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break

                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)

                # Process frame for hand tracking
                processed_frame = self.process_frame(frame)

                # Display status information
                self.display_status(processed_frame)

                # Show the frame
                cv2.imshow('AI Virtual Mouse', processed_frame)

                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == self.toggle_key:
                    self.mouse_control_enabled = not self.mouse_control_enabled
                    status = "enabled" if self.mouse_control_enabled else "disabled"
                    print(f"Mouse control {status}")

        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            print("=== Virtual Mouse Stopped ===")

if __name__ == "__main__":
    # Create and run virtual mouse
    virtual_mouse = VirtualMouse()
    virtual_mouse.run()