from django.contrib import admin

from .models import Image, ImageTag

admin.site.register(Image)
admin.site.register(ImageTag)
