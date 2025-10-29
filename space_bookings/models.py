from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from spaces.models import Space
from users.models import User


class SpaceBooking(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class BookingStatus(models.IntegerChoices):
        PENDING = 1, "Pending"
        CONFIRMED = 2, "Confirmed"
        COMPLETED = 3, "Completed"
        CANCELLED = 4, "Cancelled"

    space = models.ForeignKey(Space, related_name="bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="space_bookings", on_delete=models.CASCADE
    )
    status = models.IntegerField(
        choices=BookingStatus.choices, default=BookingStatus.PENDING
    )
    order_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["order_id"]),
        ]

    def __str__(self):
        return f"Booking of {self.space.name} by {self.user.username} with status {self.get_status_display()}"
