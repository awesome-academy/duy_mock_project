from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


def validate_location_map(value):
    if not isinstance(value, dict):
        raise serializers.ValidationError(_("Location map must be a JSON object."))

    required_keys = {"latitude", "longitude"}

    if any(key not in value for key in required_keys):
        raise serializers.ValidationError(
            _(f"Location map must contain the keys: {', '.join(required_keys)}.")
        )

    if any(not isinstance(value[key], (int, float)) for key in required_keys):
        raise serializers.ValidationError(
            _("Latitude and longitude must be numeric values.")
        )

    if abs(value["latitude"]) > 90:
        raise serializers.ValidationError(_("Latitude must be between -90 and 90."))

    if abs(value["longitude"]) > 180:
        raise serializers.ValidationError(_("Longitude must be between -180 and 180."))

    return value
