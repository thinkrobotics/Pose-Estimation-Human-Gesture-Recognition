# Real-Time Gesture Recognition using Mediapipe & OpenCV

## Overview
This project implements **real-time gesture recognition** using:
- **OpenCV** for webcam input
- **Mediapipe Pose** for human pose estimation
- **NumPy & Math** for angle calculations
- **SQLite & CSV** for gesture logging

## Features
1. **Detects Arm & Hand Gestures (Wave, Pointing, Thumbs Up, etc.)**
2. **Uses Mediapipe Pose for Landmark Detection**
3. **Logs Gesture Data to SQLite Database & CSV File**
4. **Real-time Gesture Stabilization**

## Project Structure

```
.
├── gesture_recognition.py   # Main script for real-time gesture detection
├── pose_tracking.db         # SQLite database storing pose data
├── pose_logs.csv            # CSV log of detected gestures
├── README.md                # Documentation
```

---
## Dependencies

Ensure you have Python installed (preferably 3.8+). Install required libraries:

```bash
pip install opencv-python mediapipe numpy sqlite3
```

---
## Modules Explained

### 1. `gesture_recognition.py` (Real-Time Gesture Detection)
- Captures webcam feed using **OpenCV**
- Detects **body landmarks** using **Mediapipe Pose**
- Calculates **joint angles** to classify gestures
- Stabilizes **gesture predictions** for better accuracy
- Logs **detected gestures** into SQLite & CSV

#### Key Functions:
- **calculate_angle(a, b, c)**: Computes angle between 3 points
- **detect_gestures(landmarks)**: Identifies gestures based on landmark positions
- **Logs Data**: Saves detected gestures to `pose_tracking.db` and `pose_logs.csv`

### 2. SQLite Database (`pose_tracking.db`)
- Stores each detected **gesture**, along with **elbow, shoulder, and knee angles**
- Table Structure:
  ```sql
  CREATE TABLE PoseData (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp TEXT,
      elbow_angle REAL,
      shoulder_angle REAL,
      knee_angle REAL,
      gesture TEXT
  );
  ```

### 3. CSV Logs (`pose_logs.csv`)
- Each detected **gesture** is stored with timestamp & joint angles
- Example CSV Output:
  ```csv
  Timestamp, Elbow Angle, Shoulder Angle, Knee Angle, Gesture
  2024-03-17 12:00:01, 145.2, 160.5, 178.0, Wave
  2024-03-17 12:00:02, 165.3, 150.1, 175.8, Pointing
  ```

---
## Running the Application

### 1. Start Gesture Recognition
```bash
python gesture_recognition.py
```

### 2. View SQLite Database (Optional)
```bash
sqlite3 pose_tracking.db
SELECT * FROM PoseData;
```

### 3. Analyze CSV Logs
```bash
cat pose_logs.csv
```

---
## Supported Gestures

| Gesture | Description |
|---------|------------|
| **Wave** | Both wrists above shoulders |
| **Pointing** | One arm extended with elbow angle > 160° |
| **Thumbs Up** | Wrist below elbow, elbow angle < 90° |
| **Thumbs Down** | Wrist above elbow, elbow angle < 90° |
| **Arms Crossed** | Hands crossed over chest |

---
## Troubleshooting

| Issue | Solution |
|--------|-----------|
| `cv2.VideoCapture(1)` not working | Change camera index to `0` |
| No gesture detected | Ensure good lighting & adjust webcam position |
| Gesture detection unstable | Increase `gesture_history` length for stability |

---
## Future Improvements
- **Multi-Person Gesture Recognition**
- **Hand Gesture Detection with Mediapipe Hands**
- **Real-Time Gesture Control for Applications**

---
## Credits
- **Mediapipe Pose** for Human Pose Estimation
- **OpenCV** for Image Processing
- **SQLite & CSV** for Data Logging
