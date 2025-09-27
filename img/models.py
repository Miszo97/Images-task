from uuid import uuid4

from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

# Create your models here.


def get_image_s3_file_path(instance, filename: str):
    return f"{uuid4().hex}.{filename.split('.')[-1]}"


class ImageFileS3Storage(S3Boto3Storage):
    location = "images"


class Image(models.Model):
    title = models.CharField(max_length=100)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    file = models.FileField(
        max_length=100,
        storage=ImageFileS3Storage,
        upload_to=get_image_s3_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "webp", "bmp"]
            )
        ],
    )

    def open(self) -> File:
        storage = ImageFileS3Storage()
        return storage.open(self.file.name, mode="rb")
