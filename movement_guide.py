import cv2
from scan_order import GUIDES


def draw_big_arrow(frame, direction, cx, cy):
    length = 120
    thickness = 10

    if direction == "UP":
        start, end = (cx, cy + length // 2), (cx, cy - length // 2)
    elif direction == "DOWN":
        start, end = (cx, cy - length // 2), (cx, cy + length // 2)
    elif direction == "LEFT":
        start, end = (cx + length // 2, cy), (cx - length // 2, cy)
    elif direction == "RIGHT":
        start, end = (cx - length // 2, cy), (cx + length // 2, cy)
    else:
        return

    cv2.arrowedLine(
        frame, start, end,
        (0, 0, 255), thickness,
        tipLength=0.30
    )


def draw_movement_guide(frame, face_index):
    h, w = frame.shape[:2]
    guide = GUIDES[face_index]

    panel_h = 230
    overlay = frame.copy()
    cv2.rectangle(
        overlay, (0, h - panel_h),
        (w, h), (15, 15, 15), -1
    )
    cv2.addWeighted(
        overlay, 0.92, frame, 0.08, 0, frame
    )

    cv2.putText(
        frame, f"STEP {face_index + 1} / 6",
        (30, h - 185),
        cv2.FONT_HERSHEY_SIMPLEX, 0.70,
        (0, 255, 255), 2, cv2.LINE_AA
    )

    cv2.putText(
        frame, f"SCAN: {guide['face']} FACE",
        (30, h - 145),
        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
        (0, 255, 0), 3, cv2.LINE_AA
    )

    cv2.putText(
        frame, guide["action"],
        (30, h - 105),
        cv2.FONT_HERSHEY_SIMPLEX, 0.80,
        (255, 255, 255), 2, cv2.LINE_AA
    )

    cv2.putText(
        frame, guide["detail"],
        (30, h - 65),
        cv2.FONT_HERSHEY_SIMPLEX, 0.52,
        (210, 210, 210), 1, cv2.LINE_AA
    )

    draw_big_arrow(
        frame, guide["arrow"],
        w - 125, h - 115
    )

    cv2.putText(
        frame, guide["label"],
        (w - 275, h - 35),
        cv2.FONT_HERSHEY_SIMPLEX, 0.50,
        (0, 0, 255), 2, cv2.LINE_AA
    )
