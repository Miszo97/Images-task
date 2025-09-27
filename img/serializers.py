from PIL import Image as PILImage
from PIL import UnidentifiedImageError
from rest_framework import serializers

from img.models import Image
from img.utils import resize_image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "file", "title", "width", "height"]

    def validate_file(self, file):
        stream = getattr(file, "file", file)
        try:
            img = PILImage.open(stream)
            img.verify()  # Verify the image without decoding the entire file
        except (UnidentifiedImageError, OSError, ValueError):
            raise serializers.ValidationError("Uploaded file is not a valid image.")
        finally:
            try:
                if hasattr(stream, "seek"):
                    stream.seek(0)
                if hasattr(file, "seek"):
                    file.seek(0)
            except Exception:
                pass
        return file

    def validate(self, attrs):
        width = attrs.get("width")
        height = attrs.get("height")
        if (width is None) != (height is None):
            raise serializers.ValidationError(
                "You must provide both width and height or neither."
            )
        return attrs

    def create(self, validated_data):
        file = validated_data.get("file")
        width = validated_data.get("width")
        height = validated_data.get("height")

        new_width, new_height = resize_image(file, width, height)

        validated_data["width"] = new_width
        validated_data["height"] = new_height
        return super().create(validated_data)
