from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from utils.custom_pagination import CustomPagination
from utils.permissions import IsActiveUser
from working_space_managers.models import WorkingSpaceManager
from working_spaces.filters import WorkingSpaceFilter
from working_spaces.models import WorkingSpace
from working_spaces.permissions import IsWorkingSpaceManager
from working_spaces.serializer import WorkingSpaceSerializer


class WorkingSpaceListCreateView(generics.ListCreateAPIView):
    queryset = WorkingSpace.objects.all()
    serializer_class = WorkingSpaceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WorkingSpaceFilter
    pagination_class = CustomPagination
    ordering_fields = ["name", "city", "street", "created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsActiveUser()]
        return [permissions.AllowAny()]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get("working_space", {}))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "working_space": serializer.data,
                "message": _("Working space created successfully."),
            },
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            working_space = serializer.save()
            WorkingSpaceManager.objects.create(
                working_space=working_space,
                user=self.request.user,
                role=WorkingSpaceManager.Role.ADMIN,
            )


class WorkingSpaceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkingSpace.objects.all()
    serializer_class = WorkingSpaceSerializer

    def get_object(self):
        working_space = get_object_or_404(WorkingSpace, pk=self.kwargs.get("pk", None))
        self.check_object_permissions(self.request, working_space)
        return working_space

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticatedOrReadOnly(), IsActiveUser()]
        return [
            permissions.IsAuthenticated(),
            IsActiveUser(),
            IsWorkingSpaceManager(),
        ]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(
            {
                "working_space": serializer.data,
                "message": _("Working space retrieved successfully."),
            }
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data.get("working_space", {}), partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "working_space": serializer.data,
                "message": _("Working space updated successfully."),
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            WorkingSpaceManager.objects.filter(working_space=instance).delete()
            instance.delete()
        return Response(
            {"message": _("Working space deleted successfully.")},
            status=status.HTTP_204_NO_CONTENT,
        )
