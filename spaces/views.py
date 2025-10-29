from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from space_prices.models import SpacePrice
from spaces.filters import SpaceFilter
from spaces.models import Space
from spaces.serializers.create_serializer import CreateSpaceSerializer
from spaces.serializers.infor_serializer import InforSpaceSerializer
from utils.custom_pagination import CustomPagination
from utils.permissions import IsActiveUser
from working_spaces.models import WorkingSpace


class SpaceCreateView(generics.ListCreateAPIView):
    queryset = Space.objects.all()
    serializer_class = InforSpaceSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SpaceFilter
    ordering_fields = ["name", "type", "location", "capacity"]

    def get_working_space(self):
        return get_object_or_404(
            WorkingSpace, pk=self.kwargs.get("working_space_id", None)
        )

    def get_queryset(self):
        """Get filtered queryset using FilterSet + custom prefetch for prices"""
        working_space = self.get_working_space()
        queryset = (
            super()
            .get_queryset()
            .filter(status=Space.SpaceStatus.ACTIVATED, working_space=working_space)
        )

        price_params = ["price_type", "price_min", "price_max"]
        has_price_filters = any(self.request.query_params.get(p) for p in price_params)

        if has_price_filters:
            price_conditions = self._build_price_conditions()
            price_queryset = (
                SpacePrice.objects.filter(**price_conditions)
                if price_conditions
                else SpacePrice.objects.all()
            )

            queryset = queryset.prefetch_related(
                Prefetch(
                    "space_prices",
                    queryset=price_queryset,
                    to_attr="filtered_space_prices",
                )
            )
        else:
            queryset = queryset.prefetch_related("space_prices")

        return queryset

    def _build_price_conditions(self):
        """Build price filter conditions with validation"""
        conditions = {}

        def add_condition(param, field, converter):
            if val := self.request.query_params.get(param):
                try:
                    conditions[field] = converter(val)
                except ValueError:
                    pass

        add_condition("price_type", "price_type", int)
        add_condition("price_min", "amount__gte", int)
        add_condition("price_max", "amount__lte", int)

        return conditions

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        working_space = self.get_working_space()
        serializer = CreateSpaceSerializer(data=request.data.get("space", {}))
        serializer.is_valid(raise_exception=True)
        space = serializer.save(working_space=working_space)

        return Response(
            {
                "space": serializer.data,
                "message": _("Space created successfully."),
                "space_id": space.id,
            },
            status=status.HTTP_201_CREATED,
        )
