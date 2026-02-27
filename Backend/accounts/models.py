from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Profile(models.Model):
    USER = "user"
    PROVIDER = "provider"

    ROLE_CHOICES = [
        (USER, "User"),
        (PROVIDER, "Service Provider"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)

    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    about_me = models.TextField(blank=True)

    total_rating = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.name or self.user.username


class ProviderApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_application"
    )

    #basic application (UI implementation)

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    location = models.CharField(max_length=120)
    bio = models.TextField(blank=True)

    #file upload
    credential_file = models.FileField(
        upload_to="provider_credentials/%Y/%m/",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.status}"
