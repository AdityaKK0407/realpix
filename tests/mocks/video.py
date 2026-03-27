import subprocess
import tempfile
from io import BytesIO
from pathlib import Path


def create_video(
    duration: int, codec: str, resolution: tuple[int, int], extension: str
) -> BytesIO:
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / f"video.{extension}"

        cmd = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"testsrc2=size={resolution[0]}x{resolution[1]}:rate=30",
            "-t",
            str(duration),
            "-c:v",
            codec,
            "-pix_fmt",
            "yuv420p",
            str(output),
        ]

        subprocess.run(cmd, check=True)

        bio = BytesIO(output.read_bytes())
        bio.name = f"video.{extension}"
        bio.seek(0)
        return bio


def create_large_video(
    duration: int, codec: str, resolution: tuple[int, int], extension: str
) -> BytesIO:
    while True:
        bio = create_video(duration, codec, resolution, extension)
        size = bio.seek(0, 2)
        bio.seek(0)
        if size > 50 * 1024 * 1024:
            return bio

        duration *= 2


def create_corrupted_video(
    duration: int, codec: str, resolution: tuple[int, int], extension: str
) -> BytesIO:
    video = create_video(duration, codec, resolution, extension)
    size = len(video.getvalue())
    return BytesIO(video.getvalue()[: size // 2])


def create_invalid_video_stream(
    duration: int, codec: str, _: tuple[int, int], extension: str
) -> BytesIO:
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / f"video.{extension}"

        cmd = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=1000",
            "-t",
            str(duration),
            "-c:a",
            codec,
            str(output),
        ]

        subprocess.run(cmd, check=True)

        bio = BytesIO(output.read_bytes())
        bio.name = f"video.{extension}"
        bio.seek(0)
        return bio
