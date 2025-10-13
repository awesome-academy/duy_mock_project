from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions, generics
from utils.send_mail import (
    send_verification_email,
    send_password_reset_email,
    account_activation_token,
    reset_password_token,
)
from .serializers.register_serializer import RegisterSerializer
from .serializers.profile_serializer import UserInfoSerializer
from .models import User


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get("user", {}))
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
            send_verification_email(request, user)

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
            user.status = User.UserStatus.ACTIVED
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


class PasswordResetRequestAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        try:
            user = User.objects.get(email=email)
            if (
                user.reset_password_sent_at
                and (timezone.now() - user.reset_password_sent_at).total_seconds() < 60
            ):
                return Response(
                    {
                        "error": _(
                            "A password reset email has already been sent recently. Please check your inbox."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            send_password_reset_email(request, user)
            return Response(
                {"message": _("Password reset email sent. Please check your inbox.")},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": _("User with this email does not exist.")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetConfirmAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]

    def update(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid, reset_password_token=token)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and reset_password_token.check_token(user, token):
            new_password = request.data.get("new_password", "")
            user.set_password(new_password)
            user.reset_password_token = ""
            user.reset_password_sent_at = None
            user.save()
            return Response(
                {"message": _("Password has been reset successfully.")},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": _("Password reset link is invalid or has expired.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
