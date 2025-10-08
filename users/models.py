from django.db import models


class User(models.Model):
    class UserStatus(models.IntegerChoices):
        REGISTERED = 1, "Registered"
        ACTIVED = 2, "Actived"
        DEACTIVATED = 3, "Deactivated"

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    status = models.IntegerField(
        choices=UserStatus.choices, default=UserStatus.REGISTERED
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    confirmation_token = models.CharField(max_length=255, blank=True, null=True)
    confirmation_sent_at = models.DateTimeField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            models.Index(fields=["status"]),
            models.Index(fields=["confirmation_token"]),
            models.Index(fields=["reset_password_token"]),
        ]

    def __str__(self):
        return self.username
