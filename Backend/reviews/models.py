from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    reviewer = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )

    service_provider = models.ForeignKey(
        "accounts.ServiceProvider",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "service_provider")  # unique key

    def __str__(self):
        return f"{self.reviewer} -> {self.service_provider} ({self.rating})"