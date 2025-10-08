from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from users.models import User
from working_spaces.models import WorkingSpace


class WorkingSpaceManager(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Role(models.IntegerChoices):
        ADMIN = 1, "Admin"
        MODERATOR = 2, "Moderator"

    working_space = models.ForeignKey(
        WorkingSpace, related_name="managers", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="managed_working_spaces", on_delete=models.CASCADE
    )
    role = models.IntegerField(choices=Role.choices, default=Role.MODERATOR)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("working_space", "user")
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.user.username} manages {self.working_space.name} with role {self.get_role_display()}"
