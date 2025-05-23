import cv2
import mediapipe as mp
import numpy as np
import math
import time
import csv
import json
import sqlite3
from datetime import datetime

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

conn = sqlite3.connect('pose_tracking.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS PoseData (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    elbow_angle REAL,
                    shoulder_angle REAL,
                    knee_angle REAL,
                    gesture TEXT)''')
conn.commit()

csv_filename = "pose_logs.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Elbow Angle", "Shoulder Angle", "Knee Angle", "Gesture"])

def calculate_angle(a, b, c):
    ab = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    dot_product = np.dot(ab, bc)
    mag_ab = np.linalg.norm(ab)
    mag_bc = np.linalg.norm(bc)
    angle = np.degrees(np.arccos(dot_product / (mag_ab * mag_bc)))
    return angle

def detect_gestures(landmarks):
    r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    r_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    r_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    l_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    l_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

    r_elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
    l_elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)

    # Detect "Wave"
    if r_wrist.y < r_shoulder.y - 0.05 and l_wrist.y < l_shoulder.y - 0.05:
        return "Wave"

    # Detect "Pointing"
    elif r_elbow_angle > 160 and r_wrist.y < r_shoulder.y:
        return "Pointing"

    # Detect "Thumbs Up"
    elif r_wrist.y < r_elbow.y and l_wrist.y < l_elbow.y and r_elbow_angle < 90 and l_elbow_angle < 90:
        return "Thumbs Up"

    # Detect "Thumbs Down" (New Gesture)
    elif r_wrist.y > r_elbow.y and l_wrist.y > l_elbow.y and r_elbow_angle < 90 and l_elbow_angle < 90:
        return "Thumbs Down"

    # Detect "Arms Crossed"
    elif r_wrist.x < l_shoulder.x and l_wrist.x > r_shoulder.x:
        return "Arms Crossed"

    return "None"


cap = cv2.VideoCapture(1)

with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False,
                  min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    gesture_history = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            gesture = detect_gestures(landmarks)
            gesture_history.append(gesture)
            if len(gesture_history) > 10:
                gesture_history.pop(0)
            stabilized_gesture = max(set(gesture_history), key=gesture_history.count)

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.putText(frame, f'Gesture: {stabilized_gesture}', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('Improved Gesture Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
conn.close()
