# orders/models.py
from django.db import models
from django.conf import settings
from jobs.models import Job
from django.core.validators import MinValueValidator

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders_as_customer"
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders_as_provider"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    date_completed = models.DateField()

    hired_for = models.TextField(blank=True)

    provider_rating = models.PositiveSmallIntegerField(
        null=True, blank=True
    )  # customer rates provider

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]

    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.job}"