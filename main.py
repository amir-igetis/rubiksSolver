import argparse
from solution_visualizer import show_solution

from scanner import CubeScanner
from confirmation_gui import show_confirmation
from gui_client import main as gui_main


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--gui",
        action="store_true"
    )

    args = parser.parse_args()

    if args.gui:
        gui_main()
        return

    while True:

        scanner = CubeScanner()

        scanned_faces = scanner.run()

        if not scanned_faces:
            print("\nScan cancelled.")
            return

        # Debug: verify the exact face data being passed to the confirmation GUI.
        print("\n========== BEFORE CONFIRMATION GUI ==========")
        for face in ["U", "L", "F", "R", "B", "D"]:
            print(
                f"{face}: center={scanned_faces[face][4]} | "
                f"{scanned_faces[face]}"
            )
        print("=============================================\n")

        action, confirmed_faces, result = show_confirmation(
            scanned_faces
        )

        if action == "rescan":
            print("\nRescanning...")
            continue

        if action != "solve":
            print("\nCancelled.")
            return


        print("\n" + "=" * 60)
        print("SOLUTION FOUND")
        print("=" * 60)

        print(
            "Cube string:",
            result["cube_string"]
        )

        print(
            "Moves:",
            len(result["moves"])
        )

        print(
            "Sequence:",
            result["solution"]
        )

        print("=" * 60)

        # NEW:
        # Open the visual step-by-step solution.
        show_solution(
            confirmed_faces,
            result["moves"]
        )

        return


if __name__ == "__main__":
    main()
