from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from users.models import User


class Token(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    user = models.ForeignKey(User, related_name="tokens", on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, unique=True)
    refresh_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["access_token"]),
            models.Index(fields=["refresh_token"]),
        ]

    def __str__(self):
        return f"Token for {self.user.username}"
