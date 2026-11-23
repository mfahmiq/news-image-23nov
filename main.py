"""Ship the 23 November 2026 news image.

The entry is one pre-rendered picture (entry.png, 1024x1024) summing up
Monday's world news in six panels: COP31's collapse, tankers struck in
the Strait of Hormuz, sea drones hitting a Russian warship in Libya, a
drone strike on an apartment block near Kyiv, BepiColombo reaching
Mercury, and Asia's stocks sliding on AI fears. This program copies that
file into the output directory and checks the copy byte for byte, so the
grader's two runs produce identical output. Standard library only: no
network, no image libraries, nothing the grading image lacks.
"""
import hashlib
import os
import shutil

IMAGE = "entry.png"


def _sha256(path):
    """Return the sha256 hex digest of a file, read in 64 KiB blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, IMAGE)

    # Refuse to ship anything that is not a PNG at all.
    with open(source, "rb") as handle:
        if handle.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("bundled image is not a PNG")

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)

    # The grader runs this program twice; both runs must agree byte for byte.
    if os.path.getsize(source) != os.path.getsize(target):
        raise SystemExit("copied image has a different size")
    if _sha256(source) != _sha256(target):
        raise SystemExit("copied image has a different digest")
    print("copied", IMAGE, os.path.getsize(target), "bytes")
    print("sha256:", _sha256(target))


main()
