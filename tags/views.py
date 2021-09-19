from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status

from .models import Tag
from .serializers import TagSerializer

from custom_api_key.models import CustomAPIKey
from custom_api_key.permissions import HasUserAPIKey

import logging

logger = logging.getLogger("audit")


class TagView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request: HttpRequest) -> Response:

        images: Tag = Tag.objects.all()
        logger.info(f"tag.get", extra={"user": request.user.id})
        serializer: TagSerializer = TagSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:

        name: str = request.data.get("name", "")
        description: str = request.data.get("description", "")

        try:
            tag: Tag = Tag(
                name=name,
                description=description
            )
            tag.save()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(
            f"tag.create", extra={"user": request.user.id, "payload": request.data},
        )
        return Response(TagSerializer(tag).data)

    def put(self, request: HttpRequest) -> Response:

        name: str = request.data.get("name", "")
        description: str = request.data.get("description", "")
        tag_id: int = request.data.get("id")
        user: User = CustomAPIKey.get_user(request)

        try:
            current_tag: Tag = Tag.objects.get(id=tag_id)
            current_tag.name = name
            current_tag.description = description
            current_tag.save()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(
            f"tag.update", extra={"user": user.id, "payload": request.data},
        )
        return Response(TagSerializer(current_tag).data)

    def delete(self, request: HttpRequest) -> Response:
        user: User = CustomAPIKey.get_user(request)
        tag_id: int = request.data.get("id")
        try:

            tag: Tag = get_object_or_404(Tag, id=tag_id)

            logger.info(
                f"tag.delete",
                extra={"user": user.id,
                       "tag": tag_id},
            )
            tag.delete()
        except Exception as e:
            logger.error(
                f"tag.delete",
                extra={"user": user.id,
                       "tag": tag_id},
            )
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
