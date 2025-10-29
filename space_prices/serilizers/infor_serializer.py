from rest_framework import serializers

from space_prices.models import SpacePrice


class SpacePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpacePrice
        fields = ["id", "price_type", "amount"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["price_type"] = instance.get_price_type_display()
        return representation
