from django.db import models
from accounts.models import Profile
from services.models import Service
from django.core.validators import MinValueValidator


class Job(models.Model):
    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )

    services = models.ManyToManyField(
        Service,
        related_name="jobs"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    latitude = models.FloatField(blank=True, default=33.7816133)
    longitude = models.FloatField(blank=True, default=-118.1084064)

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    is_open = models.BooleanField(default=True)

    QUOTE = "quote"
    SERVICE = "service"
    BOTH = "both"

    REQUEST_TYPE_CHOICES = [
        (QUOTE, "Looking for Quote"),
        (SERVICE, "Perform Service"),
        (BOTH, "Quote or Perform Service"),
    ]

    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        default=QUOTE
    )

    def __str__(self):
        return self.title


class JobImage(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="job_images/")

    def __str__(self):
        return f"Job {self.job.id} Image {self.id}"