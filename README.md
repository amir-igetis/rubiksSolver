# Rubik's Cube Scanner + Visual Confirmation

## Workflow

1. Run the camera scanner:
   `python main.py`
2. Scan U, R, F, D, L, B.
3. The camera window closes.
4. A visual unfolded cube appears.
5. Review all 54 detected stickers.
6. Click any incorrect sticker to cycle:
   White -> Yellow -> Red -> Orange -> Blue -> Green -> White
7. Press `SOLVE`.
8. Kociemba validates the corrected state and returns the solution.

## Physical orientation

The cube is between YOU and the CAMERA.

Start with:

- FRONT -> CAMERA
- TOP -> UP

"START POSITION" in the scanner always means exactly that.

## Run standalone confirmation GUI

```bash
python gui_client.py
```

## Install

```bash
pip install -r requirements.txt
```
