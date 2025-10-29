from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from spaces.models import Space
from users.models import User


class PaymentHistory(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class PaymentStatus(models.IntegerChoices):
        PENDING = 1, "Pending"
        COMPLETED = 2, "Completed"
        FAILED = 3, "Failed"
        REFUNDED = 4, "Refunded"

    class PaymentMethod(models.IntegerChoices):
        CREDIT_CARD = 1, "Credit Card"
        PAYEASY = 2, "PayEasy"
        CONVENIENCE_STORE = 3, "Convenience Store"

    class PaymentType(models.IntegerChoices):
        NEW = 1, "New"
        RENEWAL = 2, "Renewal"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    payment_method = models.IntegerField(
        choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD
    )
    payment_type = models.IntegerField(
        choices=PaymentType.choices, default=PaymentType.NEW
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-payment_date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["payment_method"]),
            models.Index(fields=["payment_type"]),
        ]

    def __str__(self):
        return f"Payment of {self.amount} by User {self.user.username} with status {self.get_status_display()}"
