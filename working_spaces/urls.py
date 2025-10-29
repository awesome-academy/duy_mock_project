from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from working_spaces import views

urlpatterns = [
    path(
        "working_spaces/",
        views.WorkingSpaceListCreateView.as_view(),
        name="working_space_list_create",
    ),
    path(
        "working_spaces/<int:pk>/",
        views.WorkingSpaceRetrieveUpdateDestroyView.as_view(),
        name="working_space_detail",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
