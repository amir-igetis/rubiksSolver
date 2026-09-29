from collections import Counter
import kociemba

SCAN_ORDER = ["U", "R", "F", "D", "L", "B"]


def build_cube_string(scanned_faces):
    color_to_face = {}

    for face in SCAN_ORDER:
        center_color = scanned_faces[face][4]
        if center_color in color_to_face:
            raise ValueError(
                f"Duplicate center color: {center_color}. "
                "Every face center must have a different color."
            )
        color_to_face[center_color] = face

    cube_string = ""

    for face in SCAN_ORDER:
        for color in scanned_faces[face]:
            if color not in color_to_face:
                raise ValueError(
                    f"Color {color} does not match any center color."
                )
            cube_string += color_to_face[color]

    counts = Counter(cube_string)
    bad = {
        face: counts.get(face, 0)
        for face in "URFDLB"
        if counts.get(face, 0) != 9
    }

    if bad:
        raise ValueError(
            "Each mapped face must occur exactly 9 times. "
            f"Current counts: {dict(counts)}"
        )

    return cube_string, color_to_face


def solve_cube(scanned_faces):
    cube_string, mapping = build_cube_string(scanned_faces)
    solution = kociemba.solve(cube_string)

    return {
        "cube_string": cube_string,
        "mapping": mapping,
        "solution": solution,
        "moves": solution.split(),
    }
