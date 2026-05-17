# ─────────────────────────────────────────
#  detector.py  –  EAR logic + MediaPipe
# ─────────────────────────────────────────

import cv2
import mediapipe as mp
import numpy as np
from src.config import (
    LEFT_EYE, RIGHT_EYE,
    EAR_THRESHOLD, CLOSED_FRAME_LIMIT,
    MAX_FACES, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE
)


def compute_ear(landmarks, eye_indices, frame_w, frame_h):
    """
    Eye Aspect Ratio formula:
        EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
    Returns a float. Lower = more closed.
    """
    pts = []
    for idx in eye_indices:
        lm = landmarks[idx]
        pts.append(np.array([lm.x * frame_w, lm.y * frame_h]))

    A = np.linalg.norm(pts[1] - pts[5])
    B = np.linalg.norm(pts[2] - pts[4])
    C = np.linalg.norm(pts[0] - pts[3])

    ear = (A + B) / (2.0 * C)
    return round(ear, 3)


class DrowsinessDetector:
    """
    Wraps MediaPipe FaceMesh.
    Call process_frame() on each webcam frame.
    """

    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=MAX_FACES,
            refine_landmarks=True,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE
        )
        self.closed_frames = 0
        self.total_alerts = 0

    def process_frame(self, frame):
        """
        Analyzes one BGR frame.
        Returns a dict:
            ear           - average EAR (float)
            drowsy        - True if alert should fire
            closed_frames - current consecutive closed count
            face_found    - True if a face was detected
            total_alerts  - total alerts this session
        """
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return {
                "ear": 0.0,
                "drowsy": False,
                "closed_frames": self.closed_frames,
                "face_found": False,
                "total_alerts": self.total_alerts
            }

        landmarks = results.multi_face_landmarks[0].landmark

        left_ear  = compute_ear(landmarks, LEFT_EYE,  w, h)
        right_ear = compute_ear(landmarks, RIGHT_EYE, w, h)
        avg_ear   = round((left_ear + right_ear) / 2.0, 3)

        if avg_ear < EAR_THRESHOLD:
            self.closed_frames += 1
        else:
            self.closed_frames = 0

        drowsy = self.closed_frames >= CLOSED_FRAME_LIMIT
        if drowsy:
            self.total_alerts += 1

        return {
            "ear": avg_ear,
            "drowsy": drowsy,
            "closed_frames": self.closed_frames,
            "face_found": True,
            "total_alerts": self.total_alerts
        }

    def release(self):
        self.face_mesh.close()