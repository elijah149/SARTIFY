from django.conf import settings
from django.db import models

from menu.models import Food, Vegetable


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_date = models.DateField()

    food = models.ForeignKey(
        Food,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    vegetable = models.ForeignKey(
        Vegetable,
        on_delete=models.PROTECT,
        related_name="orders",
        blank=True,
        null=True
    )

    quantity = models.PositiveIntegerField(default=1)

    special_request = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-order_date", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "order_date"],
                condition=models.Q(status__in=["pending", "confirmed", "completed"]),
                name="one_active_order_per_user_per_day"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.order_date}"
