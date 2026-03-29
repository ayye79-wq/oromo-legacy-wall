import io
import os

from django.conf import settings
from django.core.files.base import ContentFile
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

    LANG_EN = 'en'
    LANG_OM = 'om'
    LANG_CHOICES = [
        (LANG_EN, 'English'),
        (LANG_OM, 'Afaan Oromo'),
    ]

    full_name = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200, blank=True, default='')
    relationship_to_person = models.CharField(max_length=120, blank=True, default='')
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="legacies")
    story = models.TextField()
    story_en = models.TextField(blank=True, default='')
    story_om = models.TextField(blank=True, default='')
    quote = models.CharField(max_length=300, blank=True, default='')
    original_language = models.CharField(max_length=2, choices=LANG_CHOICES, default=LANG_EN)
    photo = models.ImageField(upload_to="legacy_photos/", blank=True, null=True)
    photo_enhanced = models.ImageField(upload_to="legacy_photos/", blank=True, null=True)
    photo_enhancement_status = models.CharField(
        max_length=20,
        default='none',
        choices=[
            ('none', 'Not enhanced'),
            ('pending', 'Enhancement in progress'),
            ('done', 'Enhanced'),
            ('failed', 'Enhancement failed'),
        ],
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    slug = models.SlugField(max_length=220, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"], name="legacy_status_idx"),
            models.Index(fields=["status", "-approved_at"], name="legacy_status_approved_idx"),
            models.Index(fields=["zone", "status"], name="legacy_zone_status_idx"),
            models.Index(fields=["-created_at"], name="legacy_created_idx"),
            models.Index(fields=["-approved_at"], name="legacy_approved_idx"),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.slug:
            base = slugify(self.full_name)[:180] or "legacy"
            self.slug = base
        super().save(*args, **kwargs)
        if self.photo and is_new:
            self._compress_photo()
            self._trigger_enhancement()

    def _compress_photo(self):
        try:
            from PIL import Image
            from django.core.files.storage import default_storage
            old_name = self.photo.name
            self.photo.open('rb')
            img = Image.open(self.photo)
            img.load()
            self.photo.close()
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')
            img.thumbnail((800, 1000), Image.LANCZOS)
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=82, optimize=True)
            output.seek(0)
            new_name = f"{self.slug}.jpg"
            self.photo.save(new_name, ContentFile(output.read()), save=False)
            Legacy.objects.filter(pk=self.pk).update(photo=self.photo.name)
            if old_name != self.photo.name:
                try:
                    default_storage.delete(old_name)
                except Exception:
                    pass
        except Exception:
            pass

    def _trigger_enhancement(self):
        """Fire-and-forget AI photo enhancement after save."""
        try:
            import os
            if not os.environ.get('REPLICATE_API_TOKEN'):
                return
            Legacy.objects.filter(pk=self.pk).update(photo_enhancement_status='pending')
            from .enhance import enhance_photo_async
            enhance_photo_async(self.pk)
        except Exception:
            pass

    def __str__(self):
        return self.full_name

    @property
    def candle_count(self):
        return self.tributes.filter(tribute_type=Tribute.CANDLE).count()

    @property
    def message_count(self):
        return self.tributes.filter(tribute_type=Tribute.MESSAGE).count()


class Tribute(models.Model):
    CANDLE = 'candle'
    MESSAGE = 'message'
    TYPE_CHOICES = [
        (CANDLE, 'Candle'),
        (MESSAGE, 'Message'),
    ]

    legacy = models.ForeignKey(Legacy, on_delete=models.CASCADE, related_name='tributes')
    tribute_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author_name = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tribute_type} for {self.legacy.full_name}"
