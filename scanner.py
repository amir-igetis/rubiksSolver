import cv2
import numpy as np

from color_detection import classify_roi, DISPLAY_COLORS
from movement_guide import draw_movement_guide
from scan_order import SCAN_ORDER, FACE_NAMES


class CubeScanner:
    def __init__(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not self.camera.isOpened():
            raise RuntimeError("Could not open camera.")

        self.rect_size = 60
        self.spacing = 12
        self.face_index = 0
        self.scanned_faces = {}

    def _draw_status_bar(self, frame):
        h, w = frame.shape[:2]

        cv2.rectangle(frame, (0, 0), (w, 75), (25, 25, 25), -1)

        cv2.putText(
            frame, "RUBIK'S CUBE SCANNER",
            (25, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2, cv2.LINE_AA
        )

        cv2.putText(
            frame, "SPACE = CAPTURE    Q = QUIT",
            (25, 58), cv2.FONT_HERSHEY_SIMPLEX,
            0.45, (180, 180, 180), 1, cv2.LINE_AA
        )

        bar_x, bar_y, bar_w, bar_h = w - 260, 25, 220, 18

        cv2.rectangle(
            frame, (bar_x, bar_y),
            (bar_x + bar_w, bar_y + bar_h),
            (80, 80, 80), 2
        )

        progress = int(bar_w * self.face_index / 6)
        if progress:
            cv2.rectangle(
                frame, (bar_x, bar_y),
                (bar_x + progress, bar_y + bar_h),
                (0, 200, 0), -1
            )

        cv2.putText(
            frame, f"{self.face_index}/6",
            (bar_x + bar_w + 10, bar_y + 16),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (255, 255, 255), 1, cv2.LINE_AA
        )

    def _read_face(self, frame):
        h, w = frame.shape[:2]
        grid_width = 3 * self.rect_size + 2 * self.spacing
        start_x = (w - grid_width) // 2
        start_y = (h - grid_width) // 2 - 70

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        colors = []

        for row in range(3):
            for col in range(3):
                x = start_x + col * (self.rect_size + self.spacing)
                y = start_y + row * (self.rect_size + self.spacing)

                cv2.rectangle(
                    frame, (x, y),
                    (x + self.rect_size, y + self.rect_size),
                    (255, 255, 255), 2
                )

                cx = x + self.rect_size // 2
                cy = y + self.rect_size // 2

                hsv_roi = hsv[cy - 8:cy + 8, cx - 8:cx + 8]
                bgr_roi = frame[cy - 8:cy + 8, cx - 8:cx + 8]

                color = classify_roi(hsv_roi, bgr_roi)
                colors.append(color)

                cv2.circle(
                    frame, (cx, cy), 8,
                    DISPLAY_COLORS[color], -1
                )

                cv2.putText(
                    frame, color, (x, y - 7),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45, (255, 255, 255), 1, cv2.LINE_AA
                )

        return colors, start_x, start_y

    def run(self):
        print("=" * 60)
        print("          RUBIK'S CUBE SCANNER")
        print("=" * 60)
        print()
        print("INITIAL ORIENTATION")
        print("-------------------")
        print("1. Cube is between YOU and the CAMERA.")
        print("2. FRONT face faces the CAMERA.")
        print("3. TOP face points upward.")
        print()
        print("Follow the on-screen movement guide.")
        print()

        try:
            while True:
                ok, frame = self.camera.read()
                if not ok:
                    raise RuntimeError("Could not read camera.")

                # frame = cv2.flip(frame, 1)
                colors, start_x, start_y = self._read_face(frame)
                self._draw_status_bar(frame)

                if self.face_index < 6:
                    face = SCAN_ORDER[self.face_index]

                    cv2.putText(
                        frame,
                        f"Place {FACE_NAMES[face]} face inside the grid",
                        (start_x - 80, start_y - 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 255, 0), 2, cv2.LINE_AA
                    )

                    draw_movement_guide(frame, self.face_index)

                cv2.imshow("Rubik's Cube Scanner", frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    return None

                if key == ord(" ") and self.face_index < 6:
                    if "Unknown" in colors:
                        print("[!] Cannot capture:", colors)
                        continue

                    face = SCAN_ORDER[self.face_index]
                    self.scanned_faces[face] = colors

                    print(f"[OK] Captured {FACE_NAMES[face]} face:")
                    print(colors)

                    self.face_index += 1

                    if self.face_index == 6:
                        return self.scanned_faces

        finally:
            self.camera.release()
            cv2.destroyAllWindows()
