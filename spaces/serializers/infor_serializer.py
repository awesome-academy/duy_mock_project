from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from space_prices.serilizers.infor_serializer import SpacePriceSerializer
from spaces.models import Space
from utils.validators import validate_location_map


class InforSpaceSerializer(serializers.ModelSerializer):
    location_map = serializers.JSONField(validators=[validate_location_map])
    space_prices = serializers.SerializerMethodField()

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["type"] = instance.get_type_display()
        representation["status"] = instance.get_status_display()
        return representation

    def get_space_prices(self, space_obj):
        if hasattr(space_obj, "filtered_space_prices"):
            return SpacePriceSerializer(space_obj.filtered_space_prices, many=True).data

        return SpacePriceSerializer(space_obj.space_prices, many=True).data
