from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient
from custom_api_key.models import CustomAPIKey


class APIKeyTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = APIClient()
        cls.client = APIClient()
        cls.tags_url = reverse('tag')
        user = User.objects.create(email="tst@testmail.com", username="tst@testmail.com")
        api_key, key = CustomAPIKey.objects.create_key(name="test api", user=user)

        cls.client = APIClient()
        authorized_client: APIClient = APIClient()
        authorized_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)
        cls.authorized_client = authorized_client

    def test_unauthorized_access(self):
        response: Response = self.guest_client.get(self.tags_url)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_access(self):
        response: Response = self.authorized_client.get(self.tags_url)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
