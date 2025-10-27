from django.utils.translation import gettext_lazy as _
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from space_prices.serilizers.infor_serializer import SpacePriceSerializer
from spaces.models import Space
from utils.validators import validate_location_map


class CreateSpaceSerializer(WritableNestedModelSerializer):
    location_map = serializers.JSONField(validators=[validate_location_map])
    space_prices = SpacePriceSerializer(many=True, required=False, default=[])

    class Meta:
        model = Space
        read_only_fields = ["id", "status", "working_space"]
        fields = [
            "id",
            "name",
            "status",
            "type",
            "location",
            "capacity",
            "location_map",
            "description",
            "open_time",
            "close_time",
            "space_prices",
        ]

    def validate_open_time(self, value):
        min_open_time = serializers.TimeField().to_internal_value("06:00")
        if value < min_open_time:
            raise serializers.ValidationError(
                _(f"Open time cannot be earlier than {min_open_time}.")
            )
        return value

    def validate_close_time(self, value):
        max_close_time = serializers.TimeField().to_internal_value("23:00")
        if value > max_close_time:
            raise serializers.ValidationError(
                _(f"Close time cannot be later than {max_close_time}.")
            )
        return value

    def validate(self, attrs):
        open_time = attrs.get("open_time")
        close_time = attrs.get("close_time")
        if open_time and close_time and open_time >= close_time:
            raise serializers.ValidationError(
                {"close_time": _("Close time must be later than open time.")}
            )
        return attrs
