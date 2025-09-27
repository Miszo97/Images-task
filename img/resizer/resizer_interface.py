import abc
from io import BytesIO
from typing import IO


class ImageResizer(abc.ABC):
    @abc.abstractmethod
    def resize(self, image_file: IO, width: int, height: int) -> BytesIO:
        raise NotImplementedError

    @abc.abstractmethod
    def get_image_dimensions(self, image_file: IO) -> tuple[int, int]:
        raise NotImplementedError
