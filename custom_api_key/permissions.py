from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import CustomAPIKey
import logging

logger = logging.getLogger(__name__)


class HasUserAPIKey(BaseHasAPIKey):
    model = CustomAPIKey

    def get_key(self, request):
        key = request.META.get("HTTP_AUTHORIZATION")
        if key:
            key = key.split()[1]
            try:
                api_key = CustomAPIKey.objects.get_from_key(key)
                user = api_key.user
                logger.info("api key is used " + user.username)
            except CustomAPIKey.DoesNotExist:
                logger.error("invalid API key " + key)
        return key
