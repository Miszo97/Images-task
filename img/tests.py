import os
from io import BytesIO
from unittest.mock import patch

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from img.models import Image
from img.resizer.resizer_interface import ImageResizer

pytestmark = pytest.mark.django_db


class MockImageResizer(ImageResizer):
    def resize(self, image_file, width, height) -> BytesIO:
        return BytesIO(b"resized image data")

    def get_image_dimensions(self, image_file) -> tuple[int, int]:
        return 100, 100


@pytest.fixture
def create_temp_image_file():
    file_path = os.path.join(settings.PROJECT_DIR, "test_files", "1.jpg")
    with open(file_path, "rb") as f:
        content = f.read()
    return SimpleUploadedFile(name="1.jpg", content=content, content_type="image/jpeg")


class TestImagesViewSet:
    @pytest.mark.parametrize(
        "data, attach_file,expected_error",
        [
            (
                {"title": "Title"},
                False,
                {
                    "file": [
                        ErrorDetail(string="No file was submitted.", code="required")
                    ]
                },
            ),
            (
                {},
                True,
                {
                    "title": [
                        ErrorDetail(string="This field is required.", code="required")
                    ]
                },
            ),
            (
                {"title": "Title", "width": 10},
                True,
                {
                    "non_field_errors": [
                        ErrorDetail(
                            string="You must provide both width and height or neither.",
                            code="invalid",
                        )
                    ]
                },
            ),
        ],
    )
    @patch("img.utils.get_image_resizer")
    def test_image_upload_missing_parameters(
        self,
        mock_get_image_resizer,
        client,
        create_temp_image_file,
        data,
        attach_file,
        expected_error,
    ):
        mock_get_image_resizer.return_value = MockImageResizer()
        if attach_file:
            data["file"] = create_temp_image_file
        url = reverse("images-list")
        res = client.post(url, data, format="multipart")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data == expected_error

    def test_filter_by_title_icontains(self, client):
        Image.objects.create(title="Test One", file="1.jpg")
        Image.objects.create(title="Another title", file="2.jpg")
        Image.objects.create(title="tEsT Two", file="3.jpg")

        url = reverse("images-list")
        res = client.get(url, {"title__icontains": "test"})
        assert res.status_code == status.HTTP_200_OK

        data = res.data
        results = (
            data["results"] if isinstance(data, dict) and "results" in data else data
        )
        titles = {item["title"] for item in results}
        assert titles == {"Test One", "tEsT Two"}
