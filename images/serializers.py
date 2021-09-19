from rest_framework import serializers
from .models import Image, ImageTag
from tags.models import Tag


class ImageTagSerializer(serializers.ModelSerializer):
    tagged_on = serializers.SerializerMethodField()
    name = serializers.CharField(source="tag.name")

    class Meta:
        model = ImageTag
        fields = ["id", "name", "tagged_on"]

    def get_tagged_on(self, instance):
        return instance.created_at.date()


class ImageSerializer(serializers.ModelSerializer):
    tags = ImageTagSerializer(many=True, source='imagetag_set')
    image = serializers.CharField(source="upload")

    class Meta:
        model = Image
        fields = ["id", "name", "image", "tags"]
