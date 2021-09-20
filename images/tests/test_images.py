from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient
from custom_api_key.models import CustomAPIKey

from ..models import Image

from tags.models import Tag


class ImageTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.image_url = reverse('images')
        cls.tag_url = reverse('tag')

        user = User.objects.create(email="test2@testmail.com", username="test2@testmail.com")
        api_key, key = CustomAPIKey.objects.create_key(name="test api", user=user)

        authorized_client: APIClient = APIClient()
        authorized_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)
        cls.authorized_client = authorized_client

        image_model: Image = Image(name="first image", uploader=user)
        image_model.upload = 'images/tests/sample_image.jpeg'
        image_model.save()

        image_model: Image = Image(name="second image", uploader=user)
        image_model.upload = 'images/tests/sample_image.jpeg'
        image_model.save()

        Tag.objects.create(name="first tag", description="first tag description")
        Tag.objects.create(name="second tag", description="second tag description")

    def test_get_tags(self):
        response: Response = self.authorized_client.get(self.image_url)
        # Check number of items response

        self.assertEqual(len(response.data), Image.objects.count())

    def test_invalid_tag_image(self):
        tag_image: str = reverse('tag_image', args=[1])
        response: Response = self.authorized_client.post(tag_image, {"tags": [5]})
        # Check number of items response

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_tag_image(self):
        tag_image: str = reverse('tag_image', args=[1])
        response: Response = self.authorized_client.post(tag_image, {"tags": [1]})
        # Check number of items response

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
