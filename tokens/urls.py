from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tokens import views

urlpatterns = [
    path("sign_in/", TokenObtainPairView.as_view()),
    path("refresh_token/", TokenRefreshView.as_view()),
    path("sign_out/", views.LogoutAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
