from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from tokens.models import BlacklistableAccessToken


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        try:
            refresh_token = request.data.get("refresh", None)
            if refresh_token is None:
                return Response(
                    {"detail": _("Refresh token is required.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            access_token = BlacklistableAccessToken(request.auth.token)
            access_token.blacklist()

            return Response(
                {"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
