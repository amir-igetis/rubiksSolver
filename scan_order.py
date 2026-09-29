SCAN_ORDER = ["U", "R", "F", "D", "L", "B"]

FACE_NAMES = {
    "U": "UP",
    "R": "RIGHT",
    "F": "FRONT",
    "D": "DOWN",
    "L": "LEFT",
    "B": "BACK",
}

# Physical setup:
# YOU -> CUBE -> CAMERA
#
# FRONT = face facing CAMERA
# TOP   = face pointing upward
#
# START POSITION always means:
# FRONT -> CAMERA
# TOP -> UP

GUIDES = [
    {
        "face": "UP",
        "title": "SHOW THE TOP FACE",
        "action": "TILT TOP TOWARD CAMERA",
        "detail": "Tilt the top/front edge toward the camera.",
        "arrow": "DOWN",
        "label": "TOWARD CAMERA",
    },
    {
        "face": "RIGHT",
        "title": "SHOW THE RIGHT FACE",
        "action": "RETURN TO START POSITION",
        "detail": "FRONT -> CAMERA, TOP -> UP. Then rotate to YOUR LEFT.",
        "arrow": "LEFT",
        "label": "YOUR LEFT",
    },
    {
        "face": "FRONT",
        "title": "SHOW THE FRONT FACE",
        "action": "RETURN TO START POSITION",
        "detail": "FRONT -> CAMERA, TOP -> UP.",
        "arrow": "RIGHT",
        "label": "FRONT -> CAMERA",
    },
    {
        "face": "DOWN",
        "title": "SHOW THE BOTTOM FACE",
        "action": "TILT TOP AWAY FROM CAMERA",
        "detail": "Top moves away; bottom comes toward camera.",
        "arrow": "UP",
        "label": "AWAY FROM CAMERA",
    },
    {
        "face": "LEFT",
        "title": "SHOW THE LEFT FACE",
        "action": "RETURN TO START POSITION",
        "detail": "FRONT -> CAMERA, TOP -> UP. Then rotate to YOUR RIGHT.",
        "arrow": "RIGHT",
        "label": "YOUR RIGHT",
    },
    {
        "face": "BACK",
        "title": "SHOW THE BACK FACE",
        "action": "ROTATE TO YOUR RIGHT",
        "detail": "Rotate until BACK face is facing the camera. TOP stays UP.",
        "arrow": "RIGHT",
        "label": "YOUR RIGHT",
    },
]
