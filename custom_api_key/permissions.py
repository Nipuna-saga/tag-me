from django.contrib.auth.models import User

from rest_framework.request import HttpRequest
from rest_framework_api_key.permissions import BaseHasAPIKey

from .models import CustomAPIKey

import logging

logger = logging.getLogger(__name__)


class HasUserAPIKey(BaseHasAPIKey):
    model = CustomAPIKey

    def get_key(self, request: HttpRequest) -> str:
        key: str = request.META.get("HTTP_AUTHORIZATION")
        if key:
            key: str = key.split()[1]
            try:
                api_key: CustomAPIKey = CustomAPIKey.objects.get_from_key(key)
                user: User = api_key.user
                logger.info("api key is used " + user.username)
            except CustomAPIKey.DoesNotExist:
                logger.error("invalid API key " + key)
        return key
