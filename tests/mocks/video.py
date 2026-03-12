import tempfile
import subprocess
from pathlib import Path


def create_video_file(duration: int, codec: str, extension: str) -> Path:
    tmp = tempfile.NamedTemporaryFile(suffix=f".{extension}", delete=False)
    tmp.close()

    cmd = [
        "ffmpeg",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=640x480:rate=30",
        "-t",
        str(duration),
        "-c:v",
        codec,
        tmp.name,
        "-y",
        "-loglevel",
        "error",
    ]

    subprocess.run(cmd, check=True)
    return Path(tmp.name)
