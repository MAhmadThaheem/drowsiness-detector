# ─────────────────────────────────────────
#  alert.py  –  Visual + Audio alerts
# ─────────────────────────────────────────

import cv2
import threading
import os

try:
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

from src.config import ALERT_TEXT, FONT_SCALE


ALERT_WAV = os.path.join(
    os.path.dirname(__file__), "..", "assets", "alert.wav"
)

_audio_playing = False


def _play_sound():
    global _audio_playing
    if not AUDIO_AVAILABLE:
        return
    wav = os.path.abspath(ALERT_WAV)
    if not os.path.exists(wav):
        return
    if not _audio_playing:
        _audio_playing = True
        try:
            pygame.mixer.music.load(wav)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        finally:
            _audio_playing = False


def play_alert_sound():
    """Play alert.wav in background thread — non blocking."""
    t = threading.Thread(target=_play_sound, daemon=True)
    t.start()


def draw_overlay(frame, result):
    """
    Draws all HUD elements on frame in-place.
    Shows EAR, frame counter, status, red alert if drowsy.
    """
    h, w = frame.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX

    if not result["face_found"]:
        cv2.putText(frame, "No face detected", (20, 40),
                    font, FONT_SCALE, (0, 165, 255), 2)
        return frame

    ear    = result["ear"]
    drowsy = result["drowsy"]
    closed = result["closed_frames"]

    # Status
    status_text  = "DROWSY!" if drowsy else "Awake"
    status_color = (0, 0, 220) if drowsy else (0, 200, 0)
    cv2.putText(frame, f"Status : {status_text}",
                (20, 35), font, FONT_SCALE, status_color, 2)

    # EAR value
    ear_color = (0, 0, 220) if ear < 0.25 else (0, 200, 0)
    cv2.putText(frame, f"EAR    : {ear:.3f}",
                (20, 65), font, FONT_SCALE, ear_color, 2)

    # Closed frame counter
    cv2.putText(frame, f"Frames : {closed}",
                (20, 95), font, FONT_SCALE, (200, 200, 200), 1)

    # EAR bar
    bar_x, bar_y, bar_max_w, bar_h = 20, 110, 200, 10
    fill = int(min(ear / 0.45, 1.0) * bar_max_w)
    bar_color = (0, 0, 220) if ear < 0.25 else (0, 200, 0)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + bar_max_w, bar_y + bar_h), (80, 80, 80), -1)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + fill, bar_y + bar_h), bar_color, -1)

    # Red alert overlay
    if drowsy:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 180), -1)
        cv2.addWeighted(overlay, 0.30, frame, 0.70, 0, frame)

        (tw, th), _ = cv2.getTextSize(ALERT_TEXT, font, 1.1, 3)
        tx = (w - tw) // 2
        ty = h // 2
        cv2.putText(frame, ALERT_TEXT, (tx, ty),
                    font, 1.1, (255, 255, 255), 3)

    return frame