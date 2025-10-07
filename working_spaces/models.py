from django.db import models


class WorkingSpace(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    location_map = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name
