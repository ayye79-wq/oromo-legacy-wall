from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Zone(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ZoneModerator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zones = models.ManyToManyField(Zone, related_name="moderators", blank=True)

    def __str__(self):
        return f"{self.user.username} (Zone Moderator)"


class Legacy(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    full_name = models.CharField(max_length=200)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="legacies")
    story = models.TextField()
    photo = models.ImageField(upload_to="legacy_photos/", blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    slug = models.SlugField(max_length=220, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.full_name)[:180] or "legacy"
            self.slug = base
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
