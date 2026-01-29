from django.contrib import admin
from django.utils import timezone
from .models import Legacy, Zone, ZoneModerator


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(ZoneModerator)
class ZoneModeratorAdmin(admin.ModelAdmin):
    list_display = ("user",)
    filter_horizontal = ("zones",)


@admin.register(Legacy)
class LegacyAdmin(admin.ModelAdmin):
    list_display = ("full_name", "zone", "status", "created_at", "approved_at")
    list_filter = ("status", "zone")
    search_fields = ("full_name", "story")
    readonly_fields = ("created_at", "approved_at", "slug")
    actions = ("approve_selected", "reject_selected")

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
