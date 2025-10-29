import django_filters

from .models import WorkingSpace


class WorkingSpaceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    street = django_filters.CharFilter(field_name="street", lookup_expr="icontains")

    class Meta:
        model = WorkingSpace
        fields = ["name", "city", "street", "created_at"]
        ordering = django_filters.OrderingFilter(
            fields=(
                ("name", "name"),
                ("city", "city"),
                ("street", "street"),
                ("created_at", "created_at"),
            )
        )
