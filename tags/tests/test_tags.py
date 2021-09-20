from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient
from custom_api_key.models import CustomAPIKey

from ..models import Tag


class TagsTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.tags_url = reverse('tag')
        user = User.objects.create(email="tst@testmail.com", username="tst@testmail.com")
        api_key, key = CustomAPIKey.objects.create_key(name="test api", user=user)

        authorized_client: APIClient = APIClient()
        authorized_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)
        cls.authorized_client = authorized_client

        Tag.objects.create(name="first tag", description="first tag description")
        Tag.objects.create(name="second tag", description="second tag description")

    def test_get_tags(self):
        response: Response = self.authorized_client.get(self.tags_url)
        # Check number of items response
        self.assertEqual(len(response.data), Tag.objects.count())

    def test_create_tag(self):
        new_tag: dict = {"name": "3rd tag", "description": "3rd tag description"}
        response: Response = self.authorized_client.post(self.tags_url,
                                                         data=new_tag)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_tag["name"])
        # Check number of items response
        response: Response = self.authorized_client.get(self.tags_url)
        self.assertEqual(len(response.data), Tag.objects.count())

    def test_delete_invalid_tag(self):
        tag_id: int = 5
        response: Response = self.authorized_client.delete(self.tags_url,
                                                           data={"id": tag_id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_tag(self):
        tag_id: int = 1
        response: Response = self.authorized_client.delete(self.tags_url,
                                                           data={"id": tag_id})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check number of items response
        response: Response = self.authorized_client.get(self.tags_url)
        self.assertEqual(len(response.data), Tag.objects.count())
