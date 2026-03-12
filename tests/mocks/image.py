from io import BytesIO

import numpy as np
from PIL import Image


def create_image_buffer(img_format: str) -> BytesIO:
    img = Image.new("RGB", (10, 10), color="white")
    buffer = BytesIO()
    img.save(buffer, format=img_format)
    buffer.seek(0)
    return buffer


def create_large_image_buffer(img_format: str) -> BytesIO:
    data = np.random.randint(0, 256, (2 * 1024, 2 * 1024, 3), dtype=np.uint8)
    img = Image.fromarray(data, "RGB")
    buffer = BytesIO()
    img.save(buffer, format=img_format)
    buffer.seek(0)
    return buffer


def create_image_buffer_bomb(img_format: str) -> BytesIO:
    img = Image.new("RGB", (100000, 10000), color="white")
    buffer = BytesIO()
    img.save(buffer, format=img_format, optimizer=True)
    buffer.seek(0)
    return buffer


def create_corrupt_image_buffer(img_format: str) -> BytesIO:
    buffer = create_image_buffer(img_format)
    corrupt_bytes = buffer.getvalue()[:20]
    return BytesIO(corrupt_bytes)
