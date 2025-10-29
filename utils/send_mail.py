from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator to ensure the link is single-use.
    """

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
reset_password_token = PasswordResetTokenGenerator()


def send_verification_email(request, user):
    """
    Generates and sends a verification email to the user.
    """
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    user.confirmation_token = token
    user.confirmation_sent_at = timezone.now()
    user.save()
    verification_url = f"{settings.HOST_URL}/api/verify-email/{uid}/{token}/"
    subject = "Activate Your Account"
    message = render_to_string(
        "account_verification_email.html",
        {
            "user": user,
            "verification_url": verification_url,
        },
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_password_reset_email(request, user):
    """
    Generates and sends a password reset email to the user.
    """
    token = reset_password_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    user.reset_password_token = token
    user.reset_password_sent_at = timezone.now()
    user.save()
    reset_url = f"{settings.HOST_URL}/api/reset-password/{uid}/{token}/"
    subject = "Reset Your Password"
    message = render_to_string(
        "password_reset_email.html",
        {
            "user": user,
            "reset_url": reset_url,
        },
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
