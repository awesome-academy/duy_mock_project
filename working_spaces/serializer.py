from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from utils.validators import validate_location_map
from working_spaces.models import WorkingSpace


class WorkingSpaceSerializer(serializers.ModelSerializer):
    location_map = serializers.JSONField(validators=[validate_location_map])

    class Meta:
        model = WorkingSpace
        fields = [
            "id",
            "name",
            "city",
            "street",
            "location_map",
        ]
