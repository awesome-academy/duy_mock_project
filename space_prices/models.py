from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from spaces.models import Space


class SpacePrice(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class PriceType(models.IntegerChoices):
        HOURLY = 1, "Hourly"
        DAILY = 2, "Daily"
        MONTHLY = 3, "Monthly"

    space = models.ForeignKey(
        Space, related_name="space_prices", on_delete=models.CASCADE
    )
    price_type = models.IntegerField(
        choices=PriceType.choices, default=PriceType.HOURLY
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("space", "price_type"),)
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["space"]),
            models.Index(fields=["price_type"]),
        ]

    def __str__(self):
        return f"{self.get_price_type_display()} price for space {self.space.name}: {self.amount}"
