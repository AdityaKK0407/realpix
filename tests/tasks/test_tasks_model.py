from src.tasks.model import image_task, video_task


def test_image_task() -> None:
    file_content = (b"This is an image file",)
    result = image_task(file_content)

    assert isinstance(result, list)
    assert len(result) == len(file_content)
    assert isinstance(result[0], bool)


def test_video_task() -> None:
    file_content = (b"This is a video file",)
    result = video_task(file_content)

    assert isinstance(result, list)
    assert len(result) == len(file_content)
    assert isinstance(result[0], bool)
