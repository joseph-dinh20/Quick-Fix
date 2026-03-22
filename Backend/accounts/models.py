from django.db import models
from services.models import Service
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

    city = models.CharField(max_length=50, default="Long Beach")
    state = models.CharField(max_length=100, default="California")

    latitude = models.FloatField(null=True, blank=True, default=33.7816133)
    longitude = models.FloatField(null=True, blank=True, default=-118.1084064)

    favorites = models.ManyToManyField(
        "ServiceProvider",
        related_name="favorited_by",
        blank=True
    )


    def __str__(self):
        return self.name or self.user.username
    

class WorkImage(models.Model):
    provider = models.ForeignKey("ServiceProvider", on_delete=models.CASCADE, related_name="work_images")
    image = models.ImageField(upload_to="work_photos/")

    def __str__(self):
        return f"{self.provider.profile.name} - {self.id}"
    

class ServiceProvider(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    services = models.ManyToManyField(Service, related_name="providers")

    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    about_me = models.TextField(blank=True)

    total_rating = models.IntegerField(default=0, 
                                       validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0,
                                         validators=[MinValueValidator(0), MaxValueValidator(5)]
                                         )
    
    favorited_jobs = models.ManyToManyField(
        "jobs.Job",
        related_name="favorited_by",
        blank=True
    )

    def __str__(self):
        return f"{self.profile.name} (Provider)"