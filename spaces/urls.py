from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from spaces import views

urlpatterns = [
    path(
        "working_spaces/<int:working_space_id>/spaces/",
        views.SpaceCreateView.as_view(),
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
