from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)

        jti = token["jti"]
        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            raise InvalidToken(_("Token is blacklisted"))

        return token
