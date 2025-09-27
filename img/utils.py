from django.core.files.uploadedfile import InMemoryUploadedFile

from img.resizer.pillow_resizer import PillowImageResizer
from img.resizer.resizer_interface import ImageResizer


def resize_image(
    image_file: InMemoryUploadedFile,
    width: int | None = None,
    height: int | None = None,
) -> tuple[int, int]:
    resizer: ImageResizer = get_image_resizer()
    initial_width, initial_height = resizer.get_image_dimensions(image_file=image_file)

    if (
        initial_width == width
        and initial_height == height
        or width is None
        and height is None
    ):
        return initial_width, initial_height

    binary_io = image_file.file if hasattr(image_file, "file") else image_file
    resized_img = resizer.resize(image_file=binary_io, width=width, height=height)

    image_file.file = resized_img
    try:
        image_file.size = resized_img.getbuffer().nbytes
    except Exception:
        pass

    return width, height


def get_image_resizer() -> ImageResizer:
    return PillowImageResizer()
