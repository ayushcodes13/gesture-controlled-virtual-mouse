#!/usr/bin/env python3
"""Download the official MediaPipe Hand Landmarker model with integrity checking."""

import hashlib
from pathlib import Path
from urllib.request import urlopen

URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
EXPECTED_SHA256 = "fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1"
DESTINATION = Path(__file__).resolve().parents[1] / "models" / "hand_landmarker.task"


def main() -> None:
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    temporary = DESTINATION.with_suffix(".task.part")
    digest = hashlib.sha256()
    try:
        with urlopen(URL, timeout=60) as response, temporary.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                digest.update(chunk)
                output.write(chunk)
        if digest.hexdigest() != EXPECTED_SHA256:
            raise ValueError("Downloaded model SHA-256 did not match the expected value")
        temporary.replace(DESTINATION)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Verified model saved to {DESTINATION}")


if __name__ == "__main__":
    main()
