"""Entrypoint: render the 25 November 2026 front page to entry.png.

Runs under `python3 -P -s main.py`: the script directory is NOT on
sys.path in that mode, so it is inserted here from __file__ before
importing draw. Writes /output/entry.png when /output exists (the
grader layout) and always writes entry.png beside this file.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import draw  # noqa: E402


def main():
    img = draw.render()
    local_path = os.path.join(_HERE, "entry.png")
    img.save(local_path, format="PNG", optimize=True)
    out_dir = "/output"
    if os.path.isdir(out_dir):
        img.save(os.path.join(out_dir, "entry.png"), format="PNG",
                 optimize=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
