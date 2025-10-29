import django_filters

from space_prices.models import SpacePrice

from .models import Space


class SpaceFilter(django_filters.FilterSet):
    """
    FilterSet for Space model with optimized single INNER JOIN for price filters.
    """

    name = django_filters.CharFilter(lookup_expr="icontains")
    type = django_filters.ChoiceFilter(choices=Space.SpaceType.choices)
    location = django_filters.CharFilter(lookup_expr="icontains")
    capacity = django_filters.NumberFilter(lookup_expr="gte")

    price_type = django_filters.NumberFilter(method="filter_by_prices")
    price_min = django_filters.NumberFilter(method="filter_by_prices")
    price_max = django_filters.NumberFilter(method="filter_by_prices")

    def filter_by_prices(self, queryset, name, value):
        """Custom filter method that builds a single INNER JOIN for all price filters"""

        price_conditions = {}

        def add_condition(key, field_name, converter):
            if val := self.data.get(key):
                try:
                    price_conditions[field_name] = converter(val)
                except ValueError:
                    pass

        add_condition("price_type", "space_prices__price_type", int)
        add_condition("price_min", "space_prices__amount__gte", int)
        add_condition("price_max", "space_prices__amount__lte", int)

        return (
            queryset.filter(**price_conditions).distinct()
            if price_conditions
            else queryset
        )

    class Meta:
        model = Space
        fields = [
            "name",
            "type",
            "location",
            "capacity",
            "price_min",
            "price_max",
            "price_type",
        ]
