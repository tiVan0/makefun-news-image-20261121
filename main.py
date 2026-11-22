"""Copier entrypoint for news-image-20261121 (v5-fix3).

Menyalin entry.png yang berada di direktori yang sama dengan script ini
ke direktori output yang ditunjuk variabel lingkungan
MAKEFUN_OUTPUT_DIR (default "/output") sebagai entry.png.

Hanya memakai pustaka standar Python. Tidak ada keacakan, tidak ada
tulis ke path relatif: tujuan selalu dibangun dari MAKEFUN_OUTPUT_DIR.
"""

import os
import shutil
import sys


def _script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def _output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    source = os.path.join(_script_dir(), "entry.png")
    out_dir = _output_dir()
    target = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        print("source entry.png tidak ditemukan: %s" % source,
              file=sys.stderr)
        return 1

    # Umask longgar supaya file hasil salinan bisa dibaca siapa pun,
    # lalu pastikan direktorinya ada.
    os.umask(0o022)
    os.makedirs(out_dir, exist_ok=True)

    shutil.copyfile(source, target)
    # World-readable, sesuai aturan output make.fun (0644).
    os.chmod(target, 0o644)

    print("disalin: %s -> %s" % (source, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
