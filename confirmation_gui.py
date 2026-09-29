import tkinter as tk
from tkinter import messagebox

from cube_solver import solve_cube, SCAN_ORDER

COLOR_ORDER = [
    "White",
    "Yellow",
    "Red",
    "Orange",
    "Blue",
    "Green",
]

COLOR_HEX = {
    "White": "#FFFFFF",
    "Yellow": "#FFF200",
    "Red": "#E53935",
    "Orange": "#FF9800",
    "Blue": "#1565FF",
    "Green": "#18A83A",
}

# Reference-style unfolded cube:
#
#                 U
#             L   F   R   B
#                 D
#
# This is the same visual idea as the screenshot the user supplied.
FACE_POSITIONS = {
    "U": (4, 0),
    "L": (1, 3),
    "F": (4, 3),
    "R": (7, 3),
    "B": (10, 3),
    "D": (4, 6),
}


class ConfirmationWindow:
    def __init__(self, root, scanned_faces):
        self.root = root
        self.root.title("Confirm Rubik's Cube Scan")
        self.root.geometry("1050x780")
        self.root.minsize(900, 700)
        self.confirmed = False
        self.rescan_requested = False
        self.result = None

        self.scanned_faces = {
            face: list(colors)
            for face, colors in scanned_faces.items()
        }

        self.status_var = tk.StringVar(
            value="Review every sticker, including center colors, before pressing SOLVE."
        )
        self.solution_var = tk.StringVar(
            value="Solution will appear after confirmation."
        )

        self._build()

    def _build(self):
        top = tk.Frame(self.root, bg="#202020", padx=18, pady=14)
        top.pack(fill="x")

        tk.Label(
            top,
            text="VERIFY SCANNED CUBE",
            bg="#202020",
            fg="white",
            font=("Arial", 22, "bold")
        ).pack()

        tk.Label(
            top,
            text=(
                "Check the detected colors. "
                "CLICK ANY STICKER, including centers, to cycle its color."
            ),
            bg="#202020",
            fg="#dddddd",
            font=("Arial", 11)
        ).pack(pady=(6, 0))

        body = tk.Frame(self.root, padx=20, pady=15)
        body.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            body,
            bg="#EAEAEA",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        bottom = tk.Frame(self.root, padx=20, pady=15)
        bottom.pack(fill="x")

        tk.Label(
            bottom,
            textvariable=self.status_var,
            font=("Arial", 11),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        tk.Button(
            bottom,
            text="RESCAN",
            width=12,
            command=self._rescan
        ).pack(side="right", padx=5)

        tk.Button(
            bottom,
            text="SOLVE",
            width=14,
            bg="#18A83A",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._solve
        ).pack(side="right", padx=5)

        self._draw_net()

    def _draw_net(self):
        self.canvas.delete("all")

        cell = 52
        margin_x = 70
        margin_y = 35

        # Make the net centered.
        for face, (grid_x, grid_y) in FACE_POSITIONS.items():
            colors = self.scanned_faces[face]

            for i, color in enumerate(colors):
                row = i // 3
                col = i % 3

                x1 = margin_x + (grid_x + col) * cell
                y1 = margin_y + (grid_y + row) * cell
                x2 = x1 + cell
                y2 = y1 + cell

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=COLOR_HEX[color],
                    outline="black",
                    width=2
                )

                # All stickers are editable, including the center.
                self.canvas.tag_bind(
                    rect,
                    "<Button-1>",
                    lambda event, f=face, i=i:
                    self._cycle_color(f, i)
                )

                # Show index very subtly in the corner.
                self.canvas.create_text(
                    x1 + 9, y1 + 9,
                    text=str(i + 1),
                    font=("Arial", 7),
                    fill="#555555"
                )

            self.canvas.create_text(
                margin_x + (grid_x + 1.5) * cell,
                margin_y + (grid_y + 3.22) * cell,
                text=face,
                font=("Arial", 15, "bold")
            )

        # Legend
        legend_x = 720
        legend_y = 70

        self.canvas.create_text(
            legend_x, legend_y,
            text="COLOR LEGEND",
            font=("Arial", 13, "bold")
        )

        for idx, color in enumerate(COLOR_ORDER):
            y = legend_y + 35 + idx * 42

            self.canvas.create_rectangle(
                legend_x - 55, y - 14,
                legend_x - 20, y + 21,
                fill=COLOR_HEX[color],
                outline="black",
                width=2
            )

            self.canvas.create_text(
                legend_x + 35, y + 3,
                text=color,
                font=("Arial", 11)
            )

        self.canvas.create_text(
            720, 390,
            text=(
                "Expected layout\n\n"
                "          U\n"
                "      L   F   R   B\n"
                "          D\n\n"
                "Click any sticker, including a center,\n"
                "to cycle its color."
            ),
            font=("Arial", 11),
            justify="center"
        )

    def _cycle_color(self, face, index):

        current = self.scanned_faces[face][index]

        current_index = COLOR_ORDER.index(current)

        next_index = (
                             current_index + 1
                     ) % len(COLOR_ORDER)

        new_color = COLOR_ORDER[next_index]

        self.scanned_faces[face][index] = new_color

        self.status_var.set(
            f"{face} sticker {index + 1}: "
            f"{current} → {new_color}"
        )

        self._draw_net()

    def _validate_cube(self):

        all_colors = []

        for face in SCAN_ORDER:

            if face not in self.scanned_faces:
                return False, f"Missing face: {face}"

            if len(self.scanned_faces[face]) != 9:
                return False, (
                    f"{face} has "
                    f"{len(self.scanned_faces[face])} stickers."
                )

            all_colors.extend(
                self.scanned_faces[face]
            )

        # ------------------------------------------------
        # Check color names
        # ------------------------------------------------

        for color in all_colors:

            if color not in COLOR_ORDER:
                return False, (
                    f"Invalid color detected: {color}"
                )

        # ------------------------------------------------
        # Every color must appear exactly 9 times
        # ------------------------------------------------

        for color in COLOR_ORDER:

            count = all_colors.count(color)

            if count != 9:
                return False, (
                    f"{color} appears {count} times. "
                    f"It must appear exactly 9 times."
                )

        # ------------------------------------------------
        # Centers must all be different
        # ------------------------------------------------

        centers = []

        for face in SCAN_ORDER:
            centers.append(
                self.scanned_faces[face][4]
            )

        if len(set(centers)) != 6:
            return False, (
                "The six center stickers must contain "
                "six different colors."
            )

        return True, "Cube is valid."

    def _solve(self):

        # ==================================================
        # VALIDATE CORRECTED GUI DATA
        # ==================================================

        valid, message = self._validate_cube()

        if not valid:
            messagebox.showerror(
                "Invalid Cube",
                message
            )

            self.status_var.set(
                "Cube validation failed. "
                "Correct the highlighted state."
            )

            return

        # ==================================================
        # PRINT EXACT DATA BEING SENT TO SOLVER
        # ==================================================

        print()
        print("=" * 60)
        print("CONFIRMED CUBE FROM GUI")
        print("=" * 60)

        for face in SCAN_ORDER:
            print(
                f"{face}: "
                f"{self.scanned_faces[face]}"
            )

        # ==================================================
        # CENTER MAPPING
        # ==================================================

        color_to_face = {}

        for face in SCAN_ORDER:
            center_color = (
                self.scanned_faces[face][4]
            )

            color_to_face[
                center_color
            ] = face

        print()
        print("CENTER MAPPING")
        print("-" * 40)

        for color, face in color_to_face.items():
            print(
                f"{color:10} -> {face}"
            )

        # ==================================================
        # BUILD EXACT KOCIEMBA STRING
        # ==================================================

        cube_string = ""

        for face in SCAN_ORDER:

            for color in self.scanned_faces[face]:
                cube_string += color_to_face[color]

        print()
        print("KOCIEMBA STRING")
        print("-" * 40)
        print(cube_string)

        # ==================================================
        # SOLVE
        # ==================================================

        try:

            result = solve_cube(
                self.scanned_faces
            )

        except ValueError as exc:

            print()
            print("SOLVER REJECTED:")
            print(exc)

            messagebox.showerror(
                "Kociemba Rejected Cube",
                (
                    f"{exc}\n\n"
                    f"Kociemba string:\n"
                    f"{cube_string}\n\n"
                    "Check the confirmation screen."
                )
            )

            self.status_var.set(
                "Kociemba rejected this cube state."
            )

            return

        except Exception as exc:

            messagebox.showerror(
                "Solver Error",
                str(exc)
            )

            return

        # ==================================================
        # SUCCESS
        # ==================================================

        self.result = result

        self.confirmed = True

        print()
        print("=" * 60)
        print("GUI CONFIRMATION ACCEPTED")
        print("=" * 60)

        self.root.destroy()

    def _rescan(self):
        if messagebox.askyesno(
                "Rescan",
                "Close this confirmation and scan all six faces again?"
        ):
            self.rescan_requested = True
            self.root.destroy()


def show_confirmation(scanned_faces):
    root = tk.Tk()

    window = ConfirmationWindow(
        root,
        scanned_faces
    )

    root.mainloop()

    if window.confirmed:
        return (
            "solve",
            window.scanned_faces,
            window.result
        )

    if window.rescan_requested:
        return (
            "rescan",
            None,
            None
        )

    return (
        "cancel",
        None,
        None
    )


def main():
    # Standalone demo GUI.
    demo = {
        "U": ["Yellow"] * 9,
        "R": ["Green"] * 9,
        "F": ["Red"] * 9,
        "D": ["White"] * 9,
        "L": ["Blue"] * 9,
        "B": ["Orange"] * 9,
    }

    root = tk.Tk()
    ConfirmationWindow(root, demo)
    root.mainloop()


if __name__ == "__main__":
    main()
