from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from spaces.models import Space
from users.models import User


class SpaceMember(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class MembershipStatus(models.IntegerChoices):
        INACTIVE = 1, "Inactive"
        ACTIVED = 2, "Actived"
        SUSPENDED = 3, "Suspended"

    user = models.ForeignKey(
        User, related_name="space_memberships", on_delete=models.CASCADE
    )
    space = models.ForeignKey(Space, related_name="members", on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=MembershipStatus.choices, default=MembershipStatus.INACTIVE
    )
    joined_date = models.DateField(blank=True, null=True)
    expired_date = models.DateField(blank=True, null=True)
    available_start_time = models.DateTimeField(blank=True, null=True)
    available_end_time = models.DateTimeField(blank=True, null=True)
    active_flag = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "space", "active_flag")
        ordering = ["joined_date"]
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.user.username} is a member of {self.space.name} with status {self.get_status_display()}"
