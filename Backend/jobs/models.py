from django.db import models
from accounts.models import Profile, ServiceProvider
from services.models import Service
from django.core.validators import MinValueValidator
from .utils import geolocator

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

    assigned_provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    latitude = models.FloatField(blank=True, default=33.7816133)
    longitude = models.FloatField(blank=True, default=-118.1084064)

    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

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

    FLEXIBLE = "flexible"
    SOON = "soon"
    URGENT = "urgent"

    URGENCY_CHOICES = [
        (FLEXIBLE, "Flexible"),
        (SOON, "Soon"),
        (URGENT, "Urgent"),
    ]

    urgency = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES,
        default=FLEXIBLE
    )

    language = models.ForeignKey(
        "accounts.Language",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("complete", "Complete"),
            ("cancelled", "Cancelled"),
        ],
        default="open"
    )

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude and not self.city:
            try:
                location = geolocator.reverse(f"{self.latitude}, {self.longitude}")
                if location:
                    address = location.raw.get('address', {})
                    self.city = address.get('city') or address.get('town') or address.get('village')
                    self.state = address.get('state')
                    self.zip_code = address.get('postcode')
            except Exception:
                pass  # don't block 
        super().save(*args, **kwargs)
        if not self.language and self.customer:
            first_language = self.customer.languages.first()
            if first_language:
                self.language = first_language
        super().save(*args, **kwargs)


class JobImage(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="job_images/")

    def __str__(self):
        return f"Job {self.job.id} Image {self.id}"
    

class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "provider")