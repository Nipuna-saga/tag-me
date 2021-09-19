from django.db import models
from django.contrib.auth.models import User

from rest_framework.request import HttpRequest
from rest_framework_api_key.models import AbstractAPIKey


class CustomAPIKey(AbstractAPIKey):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")

    def __str__(self):
        return f"{self.user}"

    @staticmethod
    def get_user(request: HttpRequest) -> User:
        key: str = request.META.get("HTTP_AUTHORIZATION").split()[1]
        api_key: CustomAPIKey = CustomAPIKey.objects.get_from_key(key)
        return api_key.user
