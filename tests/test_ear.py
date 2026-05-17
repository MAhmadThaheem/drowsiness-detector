# ─────────────────────────────────────────
#  tests/test_ear.py
#  Run:  python -m pytest tests/
# ─────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from src.detector import compute_ear


class FakeLandmark:
    """Mimics a MediaPipe landmark (has .x and .y)."""
    def __init__(self, x, y):
        self.x = x
        self.y = y


def make_landmarks(pts, w=640, h=480):
    """Convert pixel coords to normalized fake landmarks."""
    lms = {}
    for idx, (px, py) in pts.items():
        lms[idx] = FakeLandmark(px / w, py / h)
    return lms


def test_open_eye():
    """Wide open eye should give EAR above 0.25."""
    pts = {
        362: (200, 100),
        385: (220, 90),
        387: (240, 90),
        263: (260, 100),
        373: (240, 110),
        380: (220, 110),
    }
    lms = make_landmarks(pts)
    ear = compute_ear(lms, [362, 385, 387, 263, 373, 380], 640, 480)
    assert ear > 0.25, f"Open eye EAR should be > 0.25, got {ear}"


def test_closed_eye():
    """Nearly closed eye should give EAR below 0.25."""
    pts = {
        362: (200, 100),
        385: (220, 99),
        387: (240, 99),
        263: (260, 100),
        373: (240, 101),
        380: (220, 101),
    }
    lms = make_landmarks(pts)
    ear = compute_ear(lms, [362, 385, 387, 263, 373, 380], 640, 480)
    assert ear < 0.25, f"Closed eye EAR should be < 0.25, got {ear}"


def test_ear_symmetry():
    """Symmetric eyes should give equal EAR."""
    pts_left = {
        362: (100, 100), 385: (120, 85), 387: (140, 85),
        263: (160, 100), 373: (140, 115), 380: (120, 115),
    }
    pts_right = {
        33:  (300, 100), 160: (320, 85), 158: (340, 85),
        133: (360, 100), 153: (340, 115), 144: (320, 115),
    }
    lms = {**make_landmarks(pts_left), **make_landmarks(pts_right)}
    left_ear  = compute_ear(lms, [362, 385, 387, 263, 373, 380], 640, 480)
    right_ear = compute_ear(lms, [33, 160, 158, 133, 153, 144],  640, 480)
    assert abs(left_ear - right_ear) < 0.01, \
        f"Symmetric eyes should have equal EAR: {left_ear} vs {right_ear}"


if __name__ == "__main__":
    test_open_eye()
    test_closed_eye()
    test_ear_symmetry()
    print("All tests passed!")