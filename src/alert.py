# ─────────────────────────────────────────
#  alert.py  –  Visual + Audio alerts
# ─────────────────────────────────────────

import cv2
import threading
import os
import time

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
    t = threading.Thread(target=_play_sound, daemon=True)
    t.start()


def draw_overlay(frame, result):
    h, w = frame.shape[:2]
    font      = cv2.FONT_HERSHEY_SIMPLEX
    font_bold = cv2.FONT_HERSHEY_DUPLEX

    # ── Dark top bar ─────────────────────────────────────
    cv2.rectangle(frame, (0, 0), (w, 130), (20, 20, 20), -1)
    cv2.rectangle(frame, (0, 0), (w, 130), (50, 50, 50),  1)

    # ── Title ────────────────────────────────────────────
    cv2.putText(frame, "DROWSINESS DETECTOR",
                (12, 28), font_bold, 0.7, (255, 255, 255), 1)

    if not result["face_found"]:
        cv2.putText(frame, "No face detected — please face the camera",
                    (12, 70), font, 0.55, (0, 165, 255), 1)
        return frame

    ear    = result["ear"]
    drowsy = result["drowsy"]
    closed = result["closed_frames"]
    alerts = result["total_alerts"]

    # ── Status badge ──────────────────────────────────────
    status_text  = "DROWSY!" if drowsy else "AWAKE"
    status_color = (0, 60, 220) if drowsy else (0, 200, 80)
    badge_x = w - 140
    cv2.rectangle(frame, (badge_x, 8), (w - 10, 40), status_color, -1)
    cv2.rectangle(frame, (badge_x, 8), (w - 10, 40), (255,255,255), 1)
    cv2.putText(frame, status_text,
                (badge_x + 10, 30), font_bold, 0.6, (255, 255, 255), 1)

    # ── EAR value ─────────────────────────────────────────
    ear_color = (0, 60, 220) if ear < 0.25 else (0, 200, 80)
    cv2.putText(frame, f"EAR: {ear:.3f}",
                (12, 62), font, 0.58, ear_color, 1)

    # ── Closed frames ─────────────────────────────────────
    cv2.putText(frame, f"Closed Frames: {closed}/20",
                (12, 88), font, 0.52, (180, 180, 180), 1)

    # ── Total alerts ──────────────────────────────────────
    cv2.putText(frame, f"Alerts: {alerts}",
                (12, 112), font, 0.52, (180, 180, 180), 1)

    # ── EAR progress bar ──────────────────────────────────
    bar_x, bar_y = w - 220, 55
    bar_w, bar_h = 200, 12
    fill = int(min(ear / 0.45, 1.0) * bar_w)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + bar_w, bar_y + bar_h), (60, 60, 60), -1)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + fill, bar_y + bar_h), ear_color, -1)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + bar_w, bar_y + bar_h), (100, 100, 100), 1)
    # Threshold marker
    thresh_x = bar_x + int((0.25 / 0.45) * bar_w)
    cv2.line(frame, (thresh_x, bar_y - 3),
             (thresh_x, bar_y + bar_h + 3), (255, 255, 255), 1)
    cv2.putText(frame, "threshold",
                (thresh_x - 28, bar_y - 6), font, 0.35, (200, 200, 200), 1)
    cv2.putText(frame, "EAR level",
                (bar_x, bar_y + bar_h + 14), font, 0.38, (150, 150, 150), 1)

    # ── Closed frames bar ─────────────────────────────────
    bar2_y = bar_y + 30
    fill2  = int(min(closed / 20, 1.0) * bar_w)
    bar2_color = (0, 60, 220) if closed > 15 else (0, 180, 220)
    cv2.rectangle(frame, (bar_x, bar2_y),
                  (bar_x + bar_w, bar2_y + bar_h), (60, 60, 60), -1)
    cv2.rectangle(frame, (bar_x, bar2_y),
                  (bar_x + fill2, bar2_y + bar_h), bar2_color, -1)
    cv2.rectangle(frame, (bar_x, bar2_y),
                  (bar_x + bar_w, bar2_y + bar_h), (100, 100, 100), 1)
    cv2.putText(frame, "Drowsy frames",
                (bar_x, bar2_y + bar_h + 14), font, 0.38, (150, 150, 150), 1)

    # ── Full red alert overlay ────────────────────────────
    if drowsy:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 180), -1)
        cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)

        # Pulsing border
        cv2.rectangle(frame, (3, 3), (w - 3, h - 3), (0, 0, 255), 3)

        # Alert text centered
        alert = "!! JAAG JAO — DROWSY !!"
        (tw, th), _ = cv2.getTextSize(alert, font_bold, 1.0, 2)
        tx = (w - tw) // 2
        ty = h // 2 + 40
        # Shadow
        cv2.putText(frame, alert, (tx + 2, ty + 2),
                    font_bold, 1.0, (0, 0, 0), 3)
        # Main text
        cv2.putText(frame, alert, (tx, ty),
                    font_bold, 1.0, (255, 255, 255), 2)

    return frame