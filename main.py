"""Copy the pre-rendered news image to the grader output directory.

The entry image (entry.png, 1024x1024) is drawn at build time and ships
with this repository. This program's only job is to place it where the
grader expects it: $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Standard library only.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
