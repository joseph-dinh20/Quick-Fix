from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from jobs.models import Job


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

    job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        related_name="reviews",
        null=True,
        blank=True
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "job")

    def __str__(self):
        return f"{self.reviewer} -> {self.service_provider} ({self.rating})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_provider_rating(self.service_provider)

    def delete(self, *args, **kwargs):
        provider = self.service_provider
        super().delete(*args, **kwargs)
        self.update_provider_rating(provider)

    @staticmethod
    def update_provider_rating(provider):
        reviews = provider.reviews.all()
        count = reviews.count()
        total = reviews.aggregate(total=Sum("rating"))["total"] or 0

        provider.total_rating = total

        if count == 0:
            provider.average_rating = Decimal("0.00")
        else:
            provider.average_rating = Decimal(total) / Decimal(count)

        provider.save(update_fields=["total_rating", "average_rating"])


class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="review_images/")

    def __str__(self):
        return f"Review {self.review.id} Image {self.id}"