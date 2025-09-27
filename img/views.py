from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from img.models import Image
from img.serializers import ImageSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'head', 'options']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"title": ["icontains"]}
