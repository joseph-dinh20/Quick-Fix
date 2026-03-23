from django.db import models
from accounts.models import Profile


class Report(models.Model):
    SPAM = "spam"
    HARASSMENT = "harassment"
    FAKE_PROFILE = "fake_profile"
    INAPPROPRIATE_CONTENT = "inappropriate_content"
    SCAM = "scam"
    OTHER = "other"

    REASON_CHOICES = [
        (SPAM, "Spam"),
        (HARASSMENT, "Harassment"),
        (FAKE_PROFILE, "Fake Profile"),
        (INAPPROPRIATE_CONTENT, "Inappropriate Content"),
        (SCAM, "Scam"),
        (OTHER, "Other"),
    ]

    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (REVIEWED, "Reviewed"),
        (RESOLVED, "Resolved"),
    ]

    reporter = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="submitted_reports"
    )

    reported_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="received_reports"
    )

    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES
    )

    details = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter} reported {self.reported_profile} for {self.reason}"