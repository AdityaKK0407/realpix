from io import BytesIO

from PIL import Image


def create_image_buffer(img_format: str) -> BytesIO:
    img = Image.new("RGB", (10, 10), color="white")
    buffer = BytesIO()
    img.save(buffer, format=img_format)
    buffer.seek(0)
    return buffer


def create_corrupt_image_buffer(img_format: str) -> BytesIO:
    buffer = create_image_buffer(img_format)
    corrupt_bytes = buffer.getvalue()[:20]
    return BytesIO(corrupt_bytes)
