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


class HistoricalPeriod(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    years_label = models.CharField(max_length=40, blank=True, default='')
    years_start = models.IntegerField(null=True, blank=True)
    years_end = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, default='')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        label = f" ({self.years_label})" if self.years_label else ""
        return f"{self.name}{label}"


class HistoricalEvent(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    name = models.CharField(max_length=200)
    period = models.ForeignKey(
        HistoricalPeriod, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='events'
    )
    event_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['event_date', 'name']

    def __str__(self):
        return self.name


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

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    ]

    CATEGORY_CHOICES = [
        ('fighter', 'Fighter / Combatant'),
        ('commander', 'Commander / Military Leader'),
        ('civilian', 'Civilian'),
        ('political', 'Political Leader'),
        ('student', 'Student / Youth'),
        ('journalist', 'Journalist / Writer'),
        ('intellectual', 'Intellectual / Academic'),
        ('religious', 'Religious Leader'),
        ('cultural', 'Cultural Figure'),
        ('women', 'Women\'s Rights Leader'),
        ('lawyer', 'Lawyer / Legal Professional'),
        ('other', 'Other'),
    ]

    VERIFICATION_CHOICES = [
        ('unverified', 'Unverified'),
        ('partial', 'Partially Verified'),
        ('verified', 'Fully Verified'),
    ]

    # ── Core identity ──
    full_name = models.CharField(max_length=200)
    alternative_spellings = models.CharField(
        max_length=400, blank=True, default='',
        help_text='Comma-separated alternative name spellings'
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U', blank=True)

    # ── Dates ──
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    # ── Location ──
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="legacies")
    woreda = models.CharField(max_length=200, blank=True, default='')
    village = models.CharField(max_length=200, blank=True, default='')
    place_of_death = models.CharField(max_length=300, blank=True, default='')
    burial_location = models.CharField(max_length=300, blank=True, default='')

    # ── Classification ──
    occupation = models.CharField(max_length=200, blank=True, default='')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, blank=True, default=''
    )
    historical_period = models.ForeignKey(
        HistoricalPeriod, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='legacies'
    )
    historical_event = models.ForeignKey(
        HistoricalEvent, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='legacies'
    )

    # ── Narrative ──
    relationship_to_person = models.CharField(max_length=120, blank=True, default='')
    story = models.TextField()
    story_en = models.TextField(blank=True, default='')
    story_om = models.TextField(blank=True, default='')
    quote = models.CharField(max_length=300, blank=True, default='')
    original_language = models.CharField(max_length=2, choices=LANG_CHOICES, default=LANG_EN)
    circumstances = models.TextField(
        blank=True, default='',
        help_text='Circumstances of death or persecution'
    )
    family_notes = models.TextField(
        blank=True, default='',
        help_text='Known surviving family, relatives'
    )

    # ── Media ──
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

    # ── Research / admin ──
    notes = models.TextField(blank=True, default='', help_text='Internal research notes')
    verification_status = models.CharField(
        max_length=12, choices=VERIFICATION_CHOICES, default='unverified'
    )

    # ── Status / meta ──
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
            models.Index(fields=["historical_period", "status"], name="legacy_period_status_idx"),
            models.Index(fields=["category", "status"], name="legacy_category_status_idx"),
            models.Index(fields=["death_year"], name="legacy_death_year_idx"),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.slug:
            base = slugify(self.full_name)[:180] or "legacy"
            self.slug = base
        photo_changed = False
        if not is_new and self.photo:
            try:
                old = Legacy.objects.only('photo').get(pk=self.pk)
                photo_changed = old.photo != self.photo
            except Legacy.DoesNotExist:
                pass
        super().save(*args, **kwargs)
        if self.photo and (is_new or photo_changed):
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
        try:
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

    @property
    def lifespan(self):
        if self.birth_year and self.death_year:
            return f"{self.birth_year} – {self.death_year}"
        if self.birth_year:
            return f"b. {self.birth_year}"
        if self.death_year:
            return f"d. {self.death_year}"
        return None


class Source(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('hrw', 'Human Rights Watch'),
        ('amnesty', 'Amnesty International'),
        ('ehrc', 'Ethiopian Human Rights Council'),
        ('qeerroo', 'Qeerroo Archives'),
        ('omn', 'OMN'),
        ('addis_standard', 'Addis Standard'),
        ('bbc_om', 'BBC Afaan Oromo'),
        ('voa_om', 'VOA Afaan Oromo'),
        ('esat', 'ESAT'),
        ('academic', 'Academic Paper'),
        ('book', 'Book'),
        ('family', 'Family Submission'),
        ('cemetery', 'Cemetery Record'),
        ('newspaper', 'Newspaper'),
        ('court', 'Court Document'),
        ('other', 'Other'),
    ]

    legacy = models.ForeignKey(Legacy, on_delete=models.CASCADE, related_name='sources')
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    title = models.CharField(max_length=400, blank=True, default='')
    url = models.URLField(max_length=800, blank=True, default='')
    publication_date = models.DateField(null=True, blank=True)
    page_number = models.CharField(max_length=40, blank=True, default='')
    excerpt = models.TextField(blank=True, default='')
    uploaded_file = models.FileField(upload_to='sources/', blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['source_type', 'publication_date']

    def __str__(self):
        return f"{self.get_source_type_display()} — {self.title or self.legacy.full_name}"


class MediaItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('newspaper', 'Newspaper Clipping'),
        ('audio', 'Audio'),
    ]

    legacy = models.ForeignKey(Legacy, on_delete=models.CASCADE, related_name='media_items')
    media_type = models.CharField(max_length=12, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='legacy_media/', blank=True, null=True)
    external_url = models.URLField(max_length=800, blank=True, default='')
    caption = models.CharField(max_length=400, blank=True, default='')
    caption_om = models.CharField(max_length=400, blank=True, default='')
    media_date = models.DateField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'added_at']

    def __str__(self):
        return f"{self.get_media_type_display()} — {self.legacy.full_name}"


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
