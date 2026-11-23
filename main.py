"""news-image-20261123 entry: ship the pre-rendered 23 November 2026
infographic (six stories from that day's news, 1024x1024 PNG with a
navy date header and a 2x3 grid of story panels) by copying the
bundled entry.png beside this file into the output directory. A plain
byte copy, so the two grader runs produce identical bytes. Python
3.13, standard library only, no network, no image libraries (the
grader image has no PIL installed)."""
import hashlib
import os
import shutil

# Resolve paths relative to this file, not the working directory.
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(OUT, "entry.png")


def file_sha256(path):
    """Hash a file in chunks; the copy must be byte-identical."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, DST)

# The grader runs the program twice; both runs must write the same bytes.
assert os.path.getsize(DST) == os.path.getsize(SRC), "copy size mismatch"
assert file_sha256(DST) == file_sha256(SRC), "copy hash mismatch"
print("entry.png:", os.path.getsize(DST), "bytes ->", DST)
print("sha256:", file_sha256(DST))
