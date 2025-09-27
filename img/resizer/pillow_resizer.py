from io import BytesIO
from typing import IO

from PIL import Image as PILImage
from PIL.Image import Resampling

from img.resizer.resizer_interface import ImageResizer


class PillowImageResizer(ImageResizer):
    def resize(self, image_file: IO, width: int, height: int) -> BytesIO:
        img = PILImage.open(image_file)
        resized_img = img.resize((width, height), Resampling.LANCZOS)

        buffer = BytesIO()
        fmt = resized_img.format or "PNG"
        resized_img.save(buffer, format=fmt)
        buffer.seek(0)
        return buffer

    def get_image_dimensions(self, image_file: IO) -> tuple[int, int]:
        img = PILImage.open(image_file)
        return img.size
