# ─────────────────────────────────────────
#  main.py  –  Entry point
#  Run:  python main.py
#  Quit: press Q
# ─────────────────────────────────────────

import cv2
from src.detector import DrowsinessDetector
from src.alert import draw_overlay, play_alert_sound
from src.config import CAMERA_INDEX, WINDOW_TITLE


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam. Check CAMERA_INDEX in config.py")
        return

    detector = DrowsinessDetector()
    print("[INFO] Drowsiness Detector started. Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Core detection
        result = detector.process_frame(frame)

        # Play audio alert if drowsy
        if result["drowsy"]:
            play_alert_sound()

        # Draw HUD on frame
        frame = draw_overlay(frame, result)

        # Show window
        cv2.imshow(WINDOW_TITLE, frame)

        # Quit on Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Quitting...")
            break

    cap.release()
    detector.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()