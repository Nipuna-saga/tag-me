from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Image
from .serializers import ImageSerializer

from custom_api_key.models import CustomAPIKey
from custom_api_key.permissions import HasUserAPIKey

import logging

logger = logging.getLogger("audit")


class ImageView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request):

        images = Image.objects.all()
        logger.info(f"images.get", extra={"user": request.user.id})
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):

        name = request.data.get("name", "")
        upload = request.data['upload']
        user = CustomAPIKey.get_user(request)

        image = Image(
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

    def put(self, request):

        name = request.data.get("name", "")
        upload = request.data.get('upload')
        user = CustomAPIKey.get_user(request)
        image_id = request.data.get("id")

        try:
            current_image = Image.objects.get(id=image_id)
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

    def delete(self, request):
        user = CustomAPIKey.get_user(request)
        image_id = request.data.get("id")
        try:

            image = get_object_or_404(Image, id=image_id)

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
