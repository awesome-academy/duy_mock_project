from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from users import views

urlpatterns = [
    path("sign_up/", views.RegisterAPIView.as_view()),
    path(
        "verify-email/<str:uidb64>/<str:token>/",
        views.VerifyEmailAPIView.as_view(),
        name="verify-email",
    ),
    path("profile/", views.ProfileAPIView.as_view()),
    path("request-password-reset/", views.PasswordResetRequestAPIView.as_view()),
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        views.PasswordResetConfirmAPIView.as_view(),
        name="reset-password",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
