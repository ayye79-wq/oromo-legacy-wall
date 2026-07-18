from django.contrib import admin
from django.utils import timezone
from .models import Legacy, Zone, ZoneModerator, HistoricalPeriod, HistoricalEvent, Source, MediaItem


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(ZoneModerator)
class ZoneModeratorAdmin(admin.ModelAdmin):
    list_display = ("user",)
    filter_horizontal = ("zones",)


@admin.register(HistoricalPeriod)
class HistoricalPeriodAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "years_label", "slug")
    list_display_links = ("name",)
    ordering = ("order",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(HistoricalEvent)
class HistoricalEventAdmin(admin.ModelAdmin):
    list_display = ("name", "period", "event_date", "slug")
    list_filter = ("period",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("period",)


class SourceInline(admin.TabularInline):
    model = Source
    extra = 1
    fields = ("source_type", "title", "url", "publication_date", "page_number", "excerpt")


class MediaItemInline(admin.TabularInline):
    model = MediaItem
    extra = 1
    fields = ("media_type", "file", "external_url", "caption", "media_date", "order")


@admin.register(Legacy)
class LegacyAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "zone", "historical_period", "category",
        "birth_year", "death_year", "verification_status", "status", "created_at",
    )
    list_filter = ("status", "zone", "historical_period", "category", "gender", "verification_status")
    search_fields = ("full_name", "alternative_spellings", "story", "story_en", "story_om")
    readonly_fields = ("created_at", "approved_at", "slug")
    autocomplete_fields = ("historical_period", "historical_event")
    actions = ("approve_selected", "reject_selected", "mark_verified", "mark_partially_verified")
    inlines = [SourceInline, MediaItemInline]

    fieldsets = (
        ("Identity", {
            "fields": (
                "full_name", "alternative_spellings", "gender", "slug",
            )
        }),
        ("Dates", {
            "fields": ("birth_year", "death_year", "date_of_death"),
        }),
        ("Location", {
            "fields": ("zone", "woreda", "village", "place_of_death", "burial_location"),
        }),
        ("Classification", {
            "fields": ("occupation", "category", "historical_period", "historical_event"),
        }),
        ("Story", {
            "fields": (
                "story", "story_en", "story_om", "original_language",
                "quote", "circumstances", "family_notes",
            ),
        }),
        ("Submission", {
            "fields": ("relationship_to_person",),
        }),
        ("Photo", {
            "fields": ("photo", "photo_enhanced", "photo_enhancement_status"),
        }),
        ("Research", {
            "fields": ("notes", "verification_status"),
        }),
        ("Status", {
            "fields": ("status", "created_at", "approved_at"),
        }),
    )

    def _is_super(self, request):
        return request.user.is_superuser

    def _moderator_zones(self, request):
        try:
            zm = ZoneModerator.objects.get(user=request.user)
            return zm.zones.all()
        except ZoneModerator.DoesNotExist:
            return Zone.objects.none()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self._is_super(request):
            return qs
        zones = self._moderator_zones(request)
        return qs.filter(zone__in=zones)

    def has_change_permission(self, request, obj=None):
        if self._is_super(request) or obj is None:
            return True
        zones = self._moderator_zones(request)
        return obj.zone in zones

    def approve_selected(self, request, queryset):
        now = timezone.now()
        queryset.update(status=Legacy.STATUS_APPROVED, approved_at=now)
    approve_selected.short_description = "Approve selected legacies"

    def reject_selected(self, request, queryset):
        queryset.update(status=Legacy.STATUS_REJECTED)
    reject_selected.short_description = "Reject selected legacies"

    def mark_verified(self, request, queryset):
        queryset.update(verification_status='verified')
    mark_verified.short_description = "Mark as fully verified"

    def mark_partially_verified(self, request, queryset):
        queryset.update(verification_status='partial')
    mark_partially_verified.short_description = "Mark as partially verified"


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("legacy", "source_type", "title", "publication_date")
    list_filter = ("source_type",)
    search_fields = ("legacy__full_name", "title", "excerpt")
    autocomplete_fields = ("legacy",)


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("legacy", "media_type", "caption", "media_date", "order")
    list_filter = ("media_type",)
    search_fields = ("legacy__full_name", "caption")
    autocomplete_fields = ("legacy",)
