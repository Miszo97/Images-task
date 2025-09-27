from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "width", "height", "file")
    search_fields = ("title",)
    list_filter = ("width", "height")
    ordering = ("-id",)
