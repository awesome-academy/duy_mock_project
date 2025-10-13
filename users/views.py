from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions, generics
from utils.send_mail import send_verification_email, account_activation_token
from .serializers.register_serializer import RegisterSerializer
from .serializers.profile_serializer import UserInfoSerializer
from .models import User


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get("user", {}))
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                user = serializer.save()
                send_verification_email(request, user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "message": _(
                    "User registered successfully. Please check your email to verify your account."
                )
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid, confirmation_token=token)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.confirmation_token = ""
            user.confirmed_at = timezone.now()
            user.save()
            return Response(
                {"message": _("Email verified successfully. You can now log in.")},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": _("Activation link is invalid or has expired.")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
