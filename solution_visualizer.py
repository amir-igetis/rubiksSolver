import tkinter as tk
import copy

FACE_NORMALS = {
    "U": (0, 1, 0),
    "R": (1, 0, 0),
    "F": (0, 0, 1),
    "D": (0, -1, 0),
    "L": (-1, 0, 0),
    "B": (0, 0, -1),
}

# Kociemba facelet ordering.
# Each face is viewed directly from outside that face.
FACE_POS = {
    "U": lambda r, c: (c - 1, 1, r - 1),
    "R": lambda r, c: (1, 1 - r, 1 - c),
    "F": lambda r, c: (c - 1, 1 - r, 1),
    "D": lambda r, c: (c - 1, -1, 1 - r),
    "L": lambda r, c: (-1, 1 - r, c - 1),
    "B": lambda r, c: (1 - c, 1 - r, -1),
}

COLOR = {
    "White": "#FFFFFF",
    "Yellow": "#FFE600",
    "Red": "#E53935",
    "Orange": "#FF9800",
    "Blue": "#1976FF",
    "Green": "#19A84A",
}


def rotate_vec(v, axis, degrees):
    x, y, z = v

    if degrees == 90:
        if axis == "x":
            return (x, -z, y)
        if axis == "y":
            return (z, y, -x)
        return (-y, x, z)

    if degrees == -90:
        if axis == "x":
            return (x, z, -y)
        if axis == "y":
            return (-z, y, x)
        return (y, -x, z)

    if abs(degrees) == 180:
        if axis == "x":
            return (x, -y, -z)
        if axis == "y":
            return (-x, y, -z)
        return (-x, -y, z)

    raise ValueError(degrees)


def make_stickers(faces):
    stickers = []

    for face, values in faces.items():
        for i, color in enumerate(values):
            row, col = divmod(i, 3)

            stickers.append({
                "pos": FACE_POS[face](row, col),
                "normal": FACE_NORMALS[face],
                "color": color,
            })

    return stickers


def apply_move(stickers, move):
    face = move[0]

    suffix = move[1:] if len(move) > 1 else ""

    normal = FACE_NORMALS[face]

    if normal[0]:
        axis = "x"
        layer = normal[0]
    elif normal[1]:
        axis = "y"
        layer = normal[1]
    else:
        axis = "z"
        layer = normal[2]

    # Clockwise when looking directly at the face.
    # Positive-facing normals use -90; negative-facing normals use +90.
    quarter = (
        -90
        if normal[0] + normal[1] + normal[2] > 0
        else 90
    )

    if suffix == "2":
        angle = 180
    elif suffix == "'":
        angle = -quarter
    else:
        angle = quarter

    axis_index = {"x": 0, "y": 1, "z": 2}[axis]

    for sticker in stickers:

        if sticker["pos"][axis_index] == layer:
            sticker["pos"] = rotate_vec(
                sticker["pos"],
                axis,
                angle
            )

            sticker["normal"] = rotate_vec(
                sticker["normal"],
                axis,
                angle
            )


def stickers_to_faces(stickers):
    faces = {
        face: [None] * 9
        for face in FACE_NORMALS
    }

    normal_to_face = {
        normal: face
        for face, normal in FACE_NORMALS.items()
    }

    for sticker in stickers:

        face = normal_to_face[sticker["normal"]]

        x, y, z = sticker["pos"]

        if face == "U":
            row, col = z + 1, x + 1

        elif face == "R":
            row, col = 1 - y, 1 - z

        elif face == "F":
            row, col = 1 - y, x + 1

        elif face == "D":
            row, col = 1 - z, x + 1

        elif face == "L":
            row, col = 1 - y, z + 1

        else:  # B
            row, col = 1 - y, 1 - x

        if 0 <= row < 3 and 0 <= col < 3:
            faces[face][row * 3 + col] = sticker["color"]

    return faces


def build_states(initial_faces, moves):
    stickers = make_stickers(initial_faces)

    states = [
        stickers_to_faces(stickers)
    ]

    for move in moves:
        stickers = copy.deepcopy(stickers)

        apply_move(
            stickers,
            move
        )

        states.append(
            stickers_to_faces(stickers)
        )

    return states


class SolutionVisualizer:

    def __init__(
            self,
            root,
            initial_faces,
            moves
    ):

        self.root = root
        self.moves = moves

        self.states = build_states(
            initial_faces,
            moves
        )

        self.root.title(
            "Rubik's Cube - Solution Steps"
        )

        self.root.geometry(
            "1450x900"
        )

        self.root.configure(
            bg="#eeeeee"
        )

        # -------------------------
        # HEADER
        # -------------------------

        header = tk.Frame(
            root,
            bg="#eeeeee"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 8)
        )

        tk.Label(
            header,
            text="SOLUTION STEPS",
            bg="#eeeeee",
            font=("Arial", 24, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            header,
            text=(
                f"{len(moves)} moves  •  "
                "Scroll to view every step"
            ),
            bg="#eeeeee",
            fg="#555555",
            font=("Arial", 11)
        ).pack(
            anchor="w"
        )

        # -------------------------
        # SCROLLABLE AREA
        # -------------------------

        outer = tk.Frame(
            root,
            bg="#eeeeee"
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.canvas = tk.Canvas(
            outer,
            bg="#eeeeee",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            outer,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.draw_cards()

    # ------------------------------------------------
    # 3D ISOMETRIC PROJECTION
    # ------------------------------------------------

    def project(
            self,
            x,
            y,
            z,
            cx,
            cy,
            scale=48
    ):

        return (
            cx + (x - z) * scale,
            cy
            - y * scale * 0.95
            + (x + z) * scale * 0.42
        )

    # ------------------------------------------------
    # CREATE ONE STICKER POLYGON
    # ------------------------------------------------

    def sticker_poly(
            self,
            face,
            row,
            col,
            cx,
            cy,
            scale=48
    ):

        if face == "U":

            x0 = -1 + 2 * col / 3
            x1 = -1 + 2 * (col + 1) / 3

            z0 = -1 + 2 * row / 3
            z1 = -1 + 2 * (row + 1) / 3

            pts3 = [
                (x0, 1, z0),
                (x1, 1, z0),
                (x1, 1, z1),
                (x0, 1, z1)
            ]

        elif face == "F":

            x0 = -1 + 2 * col / 3
            x1 = -1 + 2 * (col + 1) / 3

            y1 = 1 - 2 * row / 3
            y0 = 1 - 2 * (row + 1) / 3

            pts3 = [
                (x0, y0, 1),
                (x1, y0, 1),
                (x1, y1, 1),
                (x0, y1, 1)
            ]

        else:  # RIGHT

            z1 = 1 - 2 * col / 3
            z0 = 1 - 2 * (col + 1) / 3

            y1 = 1 - 2 * row / 3
            y0 = 1 - 2 * (row + 1) / 3

            pts3 = [
                (1, y0, z0),
                (1, y0, z1),
                (1, y1, z1),
                (1, y1, z0)
            ]

        return [
            self.project(
                *point,
                cx,
                cy,
                scale
            )
            for point in pts3
        ]

    # ------------------------------------------------
    # DRAW CUBE
    # ------------------------------------------------

    def draw_cube(
            self,
            x,
            y,
            faces,
            move=None
    ):

        cx = x
        cy = y + 100

        # Draw visible faces.
        for face in ("U", "F", "R"):

            for row in range(3):

                for col in range(3):
                    polygon = self.sticker_poly(
                        face,
                        row,
                        col,
                        cx,
                        cy
                    )

                    color = COLOR[
                        faces[face][row * 3 + col]
                    ]

                    self.canvas.create_polygon(
                        polygon,
                        fill=color,
                        outline="#111111",
                        width=2
                    )

        # Outer cube edges.
        corners = [

            self.project(
                -1, 1, -1,
                cx, cy
            ),

            self.project(
                1, 1, -1,
                cx, cy
            ),

            self.project(
                1, 1, 1,
                cx, cy
            ),

            self.project(
                -1, 1, 1,
                cx, cy
            ),

            self.project(
                -1, -1, 1,
                cx, cy
            ),

            self.project(
                1, -1, 1,
                cx, cy
            ),

            self.project(
                1, -1, -1,
                cx, cy
            ),
        ]

        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (3, 4),
            (2, 5),
            (5, 6),
            (1, 6)
        ]

        for a, b in edges:
            self.canvas.create_line(
                *corners[a],
                *corners[b],
                fill="#111111",
                width=2
            )

        if move:
            self.draw_move_marker(
                move,
                cx,
                cy
            )

    # ------------------------------------------------
    # MOVE INDICATOR
    # ------------------------------------------------

    def draw_move_marker(
            self,
            move,
            cx,
            cy
    ):

        face = move[0]

        if face not in ("U", "F", "R"):
            return

        centers = {
            "U": (0, 1.03, 0),
            "F": (0, 0, 1.03),
            "R": (1.03, 0, 0)
        }

        px, py = self.project(
            *centers[face],
            cx,
            cy,
            48
        )

        self.canvas.create_oval(
            px - 20,
            py - 20,
            px + 20,
            py + 20,
            fill="white",
            outline="#111111",
            width=2
        )

        if len(move) > 1 and move[1] == "2":
            label = "2X"
        elif "'" in move:
            label = "↺"
        else:
            label = "↻"

        self.canvas.create_text(
            px,
            py,
            text=label,
            font=("Arial", 18, "bold"),
            fill="#111111"
        )

    # ------------------------------------------------
    # DRAW ALL STEP CARDS
    # ------------------------------------------------

    def draw_cards(self):

        columns = 4

        card_w = 275
        card_h = 310

        gap_x = 18
        gap_y = 18

        margin_x = 12
        margin_y = 12

        for i, state in enumerate(
                self.states
        ):

            col = i % columns
            row = i // columns

            x0 = (
                    margin_x
                    + col * (card_w + gap_x)
            )

            y0 = (
                    margin_y
                    + row * (card_h + gap_y)
            )

            # Card background.
            self.canvas.create_rectangle(
                x0,
                y0,
                x0 + card_w,
                y0 + card_h,
                fill="#f8f8f8",
                outline="#dddddd"
            )

            # Move title.
            if i == 0:
                title = "Start"
            else:
                title = (
                    f"{i}: "
                    f"{self.moves[i - 1]}"
                )

            self.canvas.create_text(
                x0 + 14,
                y0 + 25,
                text=title,
                anchor="w",
                font=("Arial", 17, "bold"),
                fill="#333333"
            )

            # Cube.
            self.draw_cube(
                x0 + card_w / 2,
                y0 + 35,
                state,
                None if i == 0
                else self.moves[i - 1]
            )

        total_rows = (
                             len(self.states)
                             + columns - 1
                     ) // columns

        total_height = (
                margin_y
                + total_rows * (card_h + gap_y)
                + 20
        )

        self.canvas.configure(
            scrollregion=(
                0,
                0,
                columns * (card_w + gap_x),
                total_height
            )
        )


def show_solution(
        initial_faces,
        moves
):
    root = tk.Tk()

    SolutionVisualizer(
        root,
        initial_faces,
        moves
    )

    root.mainloop()
