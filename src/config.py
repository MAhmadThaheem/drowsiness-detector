# ─────────────────────────────────────────
#  config.py  –  All tunable settings
#  Change values here, nowhere else.
# ─────────────────────────────────────────

# EAR threshold — below this = eye considered closed
EAR_THRESHOLD = 0.25

# How many consecutive closed frames before alert fires
CLOSED_FRAME_LIMIT = 20

# Webcam index (0 = default laptop cam)
CAMERA_INDEX = 0

# Display window title
WINDOW_TITLE = "Drowsiness Detector"

# Alert message shown on screen
ALERT_TEXT = "JAAG JAO!  -  Alert!"

# Font scale for on-screen text
FONT_SCALE = 0.65

# MediaPipe face mesh settings
MAX_FACES = 1
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.7

# Eye landmark indices (MediaPipe 468-point model)
# Left eye
LEFT_EYE = [362, 385, 387, 263, 373, 380]
# Right eye
RIGHT_EYE = [33, 160, 158, 133, 153, 144]