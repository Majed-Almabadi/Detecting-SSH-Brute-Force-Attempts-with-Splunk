# README visuals

- `hero.png`: project banner.
- `investigation.gif`: four stages at 20 frames per second, looping every 8 seconds.
- `process.png`: all four stages in a static image.

To regenerate, install Python 3 and Pillow (`python -m pip install Pillow`), then run `python scripts/generate_visuals.py` from the repository root. The script uses Segoe UI on Windows, DejaVu Sans on Linux, or Pillow's default font. No network access is used during generation. Text and colors can be edited in the script. Generated assets are committed so README viewing needs no build step.
