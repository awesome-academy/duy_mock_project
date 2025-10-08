from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from working_spaces.models import WorkingSpace


class Amenity(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(max_length=255)
    working_space = models.ForeignKey(
        WorkingSpace, related_name="amenities", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name + " at " + self.working_space.name
