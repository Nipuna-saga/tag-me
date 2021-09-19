from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from datetime import datetime

from .models import Image, ImageTag
from .serializers import ImageSerializer

from tags.models import Tag

from custom_api_key.models import CustomAPIKey
from custom_api_key.permissions import HasUserAPIKey

import logging

logger = logging.getLogger("audit")


class ImageView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request: HttpRequest) -> Response:

        tagged_on = request.GET.get('tagged_on', None)

        try:
            q = Q()

            if tagged_on:
                datetime_object = datetime.strptime(tagged_on, '%Y-%m-%d')
                q.add(Q(imagetag__created_at__year=datetime_object.year), Q.AND)
                q.add(Q(imagetag__created_at__month=datetime_object.month), Q.AND)
                q.add(Q(imagetag__created_at__day=datetime_object.day), Q.AND)

            images: Image = Image.objects.filter(q).distinct()
            logger.info(f"images.get", extra={"user": request.user.id})
            serializer: ImageSerializer = ImageSerializer(images, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest) -> Response:

        name: str = request.data.get("name", "")
        upload: str = request.data['upload']
        user: User = CustomAPIKey.get_user(request)

        image: Image = Image(
            name=name,
            upload=upload,
            uploader=user
        )

        try:
            image.save()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(
            f"image.create", extra={"user": request.user.id, "payload": request.data},
        )
        return Response(ImageSerializer(image).data)

    def put(self, request: HttpRequest) -> Response:

        name: str = request.data.get("name", "")
        upload: str = request.data.get('upload')
        user: User = CustomAPIKey.get_user(request)
        image_id: int = request.data.get("id")

        try:
            current_image: Image = Image.objects.get(id=image_id)
            current_image.name = name
            if upload:
                current_image.upload = upload
            current_image.uploader = user

            current_image.save()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(
            f"image.update", extra={"user": request.user.id, "payload": request.data},
        )
        return Response(ImageSerializer(current_image).data)

    def delete(self, request: HttpRequest) -> Response:
        user: User = CustomAPIKey.get_user(request)
        image_id: int = request.data.get("id")
        try:

            image: Image = get_object_or_404(Image, id=image_id)

            logger.info(
                f"image.delete",
                extra={"user": user.id,
                       "image": image_id},
            )
            image.delete()
        except Exception as e:
            logger.error(
                f"image.delete",
                extra={"user": user.id,
                       "image": image_id},
            )
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([HasUserAPIKey])
def tag_image(request: HttpRequest, image_id: str) -> Response:
    user: User = CustomAPIKey.get_user(request)
    try:
        image: Image = get_object_or_404(Image, id=image_id)
        tags = request.data.get("tags", [])
        image.tags.clear()
        for tag in tags:
            tag = Tag.objects.get(id=tag)
            ImageTag.objects.create(tag=tag, image=image, tagged_by=user)
        logger.info(
            f"image.tag.create",
            extra={"user": user.id,
                   "image": image_id,
                   "tags": tags},
        )
    except Exception as e:
        logger.error(
            f"image.tag.create",
            extra={"user": user.id,
                   "image": image_id},
        )
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
