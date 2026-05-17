# 😴 Drowsiness Detector

> Real-time driver drowsiness detection using Computer Vision — no dataset training required.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.11-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📌 Overview

**Drowsiness Detector** is a real-time Computer Vision system that monitors a driver's eye activity through a webcam and triggers an audio-visual alert when drowsiness is detected.

It uses **MediaPipe's 468-point Face Mesh** to extract eye landmarks and computes the **Eye Aspect Ratio (EAR)** — a proven metric from academic research — to determine whether eyes are open or closed. No custom model training or GPU required.

---

## 🎯 Problem Statement

Driver fatigue is one of the leading causes of road accidents globally. Drowsy driving causes thousands of accidents every year. This project provides a lightweight, real-time software solution that runs on any standard laptop with a webcam — no expensive hardware needed.

---

## ✨ Features

- ✅ Real-time eye detection via webcam
- ✅ EAR (Eye Aspect Ratio) calculation for both eyes
- ✅ Consecutive closed-frame counter
- ✅ Visual HUD — EAR bar, status badge, frame counter
- ✅ Full-screen red alert overlay when drowsiness detected
- ✅ Audio alert — "Jaag Jao!" (Urdu warning)
- ✅ Configurable thresholds via `config.py`
- ✅ Unit tested core logic
- ✅ No GPU required — runs on CPU only

---

## 🧠 How It Works

```
Webcam Feed
    │
    ▼
MediaPipe FaceMesh
(468 face landmarks per frame)
    │
    ▼
Extract 6 Eye Landmarks
(per eye — left & right)
    │
    ▼
Compute EAR Formula
EAR = (|p2−p6| + |p3−p5|) / (2 × |p1−p4|)
    │
    ▼
EAR < 0.20 for 30+ consecutive frames?
    │
   YES → Fire Alert (Visual + Audio)
    NO → Continue monitoring
```

### EAR Formula Explained

The Eye Aspect Ratio (EAR) was introduced by Soukupová & Čech (2016). When the eye is open, EAR stays around **0.25–0.35**. When closed, it drops near **0.0**.

```
        p2    p3
    p1            p4
        p6    p5

EAR = (‖p2−p6‖ + ‖p3−p5‖) / (2 × ‖p1−p4‖)
```

---

## 🗂️ Project Structure

```
drowsiness-detector/
│
├── src/
│   ├── __init__.py        # Package init
│   ├── config.py          # All thresholds and settings
│   ├── detector.py        # EAR logic + MediaPipe wrapper
│   └── alert.py           # Visual HUD + audio alert system
│
├── assets/
│   └── alert.wav          # Urdu audio alert
│
├── tests/
│   └── test_ear.py        # Unit tests for EAR calculation
│
├── main.py                # Entry point — run this
├── requirements.txt       # Dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration

All tunable parameters are in `src/config.py` — change values there only:

| Parameter | Default | Description |
|---|---|---|
| `EAR_THRESHOLD` | `0.20` | EAR below this = eye considered closed |
| `CLOSED_FRAME_LIMIT` | `30` | Consecutive closed frames before alert fires |
| `CAMERA_INDEX` | `0` | Webcam device index |
| `MAX_FACES` | `1` | Max faces to detect |
| `DETECTION_CONFIDENCE` | `0.7` | MediaPipe detection confidence |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10
- Anaconda
- Webcam

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/drowsiness-detector.git
cd drowsiness-detector

# 2. Create conda environment
conda create -n drowsiness python=3.10
conda activate drowsiness

# 3. Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

Press **Q** to quit.

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

Three unit tests verify the EAR calculation:
- `test_open_eye` — EAR > 0.25 for wide open eye
- `test_closed_eye` — EAR < 0.25 for closed eye
- `test_ear_symmetry` — symmetric eyes give equal EAR

---

## 📦 Dependencies

```
opencv-python>=4.8.0
mediapipe==0.10.11
pygame>=2.5.0
numpy>=1.24.0
pytest>=7.0.0
```

---

## 🛣️ Future Improvements

- [ ] Head pose estimation (nodding detection)
- [ ] Session logging — alert history saved to CSV
- [ ] Packaging as standalone `.exe` for Windows

---

## 🙋‍♂️ Author

**M Ahmad**
BS Software Engineering — FAST-NUCES
[GitHub](https://github.com/MAhmadThaheem) • [LinkedIn](https://linkedin.com/in/MAhmadThaheem)

---

> *"Built to solve a real problem — driver fatigue detection without any expensive hardware or model training."*
