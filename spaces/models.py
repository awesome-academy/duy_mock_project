from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from working_spaces.models import WorkingSpace


class Space(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class SpaceStatus(models.IntegerChoices):
        WAITING = 1, "Waiting"
        ACTIVATED = 2, "Activated"
        BLOCKED = 3, "Blocked"

    class SpaceType(models.IntegerChoices):
        PRIVATE_OFFICE = 1, "Private Office"
        MEETING_ROOM = 2, "Meeting Room"
        HOT_DESK = 3, "Hot Desk"

    name = models.CharField(max_length=255)
    working_space = models.ForeignKey(
        WorkingSpace, related_name="spaces", on_delete=models.CASCADE
    )
    status = models.IntegerField(
        choices=SpaceStatus.choices, default=SpaceStatus.WAITING
    )
    type = models.IntegerField(
        choices=SpaceType.choices, default=SpaceType.PRIVATE_OFFICE
    )
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    location_map = models.JSONField(default=dict)
    description = models.TextField(blank=True, null=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ("working_space", "name")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["status"]),
            models.Index(fields=["type"]),
        ]

    def __str__(self):
        return self.name
