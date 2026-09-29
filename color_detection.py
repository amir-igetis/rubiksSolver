import cv2
import numpy as np


def get_color_name(h, s, v, b, g, r):
    """
    Detect sticker color.

    White/blue are deliberately separated using both HSV and
    BGR information because daylight can make white look blue.
    """
    total = float(b + g + r) + 1e-6
    blue_ratio = b / total
    rgb_spread = max(b, g, r) - min(b, g, r)

    # White: bright + low saturation + reasonably neutral RGB.
    if (
        v > 125
        and s < 75
        and rgb_spread < 55
        and blue_ratio < 0.42
    ):
        return "White"

    # Blue: hue plus actual blue-channel dominance.
    if (
        90 <= h <= 135
        and s > 55
        and b > r * 1.20
        and b > g * 1.05
    ):
        return "Blue"

    if (h < 5 or h > 165) and s > 60:
        return "Red"

    if 5 <= h < 25 and s > 60:
        return "Orange"

    if 25 <= h < 45 and s > 60:
        return "Yellow"

    if 45 <= h < 90 and s > 50:
        return "Green"

    return "Unknown"


def classify_roi(hsv_roi, bgr_roi):
    hsv = np.median(hsv_roi, axis=(0, 1))
    bgr = np.median(bgr_roi, axis=(0, 1))

    return get_color_name(
        float(hsv[0]), float(hsv[1]), float(hsv[2]),
        float(bgr[0]), float(bgr[1]), float(bgr[2])
    )


DISPLAY_COLORS = {
    "White": (255, 255, 255),
    "Red": (0, 0, 255),
    "Orange": (0, 165, 255),
    "Yellow": (0, 255, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Unknown": (128, 128, 128),
}
