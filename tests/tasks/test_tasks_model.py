from src.tasks.model import image_task


def test_image_task():
    filepath = "image.png"
    file_content = b"This is an image file"
    result = image_task(filepath, file_content)

    assert isinstance(result, dict)
    assert isinstance(result["filepath"], str)
    assert isinstance(result["content_size"], int)
    assert result["filepath"] == filepath
    assert result["content_size"] == len(file_content)


#
# def test_video_task():
#     filepath = "video.mp4"
#     file_content = b"This is an video file"
#     result = video_task(filepath, file_content)
#
#     assert isinstance(result, dict)
#     assert isinstance(result["filepath"], str)
#     assert isinstance(result["content_size"], int)
#     assert result["filepath"] == filepath
#     assert result["content_size"] == len(file_content)
