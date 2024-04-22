from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import UserAPIKey, APIAccessLog
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        endpoint = request.path  # Capture the request path
        if not api_key:
            self.log_api_access(None, endpoint, success=False)
            return None

        try:
            # Attempt to retrieve the API key while ensuring it is a valid UUID
            key = UserAPIKey.objects.get(key=api_key, user__is_active=True)
            self.log_api_access(key, endpoint, success=True)
            return (key.user, None)
        except UserAPIKey.DoesNotExist:
            self.log_api_access(None, endpoint, success=False)
            raise AuthenticationFailed('Invalid API Key')
        except ValidationError:
            self.log_api_access(None, endpoint, success=False)
            raise AuthenticationFailed('Invalid API Key')

    def log_api_access(self, api_key, endpoint, success):
        APIAccessLog.objects.create(
            api_key=api_key,
            accessed_at=now(),
            endpoint=endpoint,
            success=success
        )
