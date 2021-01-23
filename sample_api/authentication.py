from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted")

        if self._is_token_expired(token):
            token.delete()
            Token.objects.create(user=token.user)
            raise AuthenticationFailed("Token has expired")
        return (token.user, token)


    def _is_token_expired(self, token):
        min_age = timezone.now() - timedelta(
            seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
        return token.created < min_age
