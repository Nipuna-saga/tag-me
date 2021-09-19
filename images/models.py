from django.db import models
from django.contrib.auth.models import User

from tags.models import Tag

import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'data/user_{0}/{1}'.format(instance.uploader.id, filename)


class Image(models.Model):
    name = models.CharField(max_length=100)
    upload = models.ImageField(upload_to=user_directory_path)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag, through='ImageTag', related_name='images')

    def __str__(self):
        return self.name


class ImageTag(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    tagged_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags", null=True, blank=True)

    def __str__(self):
        return f"{self.image.name} - {self.tag.name} - {self.tagged_by.username}"
