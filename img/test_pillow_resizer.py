import os
from io import BytesIO

import pytest
from PIL import Image as PILImage

from img.resizer.pillow_resizer import PillowImageResizer


@pytest.fixture(scope="module")
def image_paths():
    project_root = os.path.dirname(os.path.dirname(__file__))
    tf = os.path.join(project_root, "test_files")
    return [
        os.path.join(tf, "1.jpg"),
        os.path.join(tf, "1.png"),
        os.path.join(tf, "2.jpg"),
    ]


class TestPillowImageResizer:
    @pytest.mark.parametrize("target_size", [(32, 32), (120, 80), (1, 1)])
    def test_resize_returns_image_with_expected_dimensions_and_png_format(
        self, image_paths, target_size
    ):
        width, height = target_size
        resizer = PillowImageResizer()

        for path in image_paths:
            with open(path, "rb") as f:
                out: BytesIO = resizer.resize(f, width, height)

            assert isinstance(out, BytesIO)
            assert out.tell() == 0

            with PILImage.open(out) as img:
                assert img.size == (width, height)
                assert img.format == "PNG"

    def test_get_image_dimensions_matches_pillow_open(self, image_paths):
        resizer = PillowImageResizer()

        for path in image_paths:
            with open(path, "rb") as f:
                expected_size = PILImage.open(f).size
                f.seek(0)
                got_size = resizer.get_image_dimensions(f)
            assert got_size == expected_size
