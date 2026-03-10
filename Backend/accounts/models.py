from django.db import models
from services.models import Service
from django.contrib.auth.models import User

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
    

class ServiceProvider(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    services = models.ManyToManyField(Service, related_name="providers")

    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    about_me = models.TextField(blank=True)

    total_rating = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)