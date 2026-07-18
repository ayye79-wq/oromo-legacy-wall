import os
from rest_framework import serializers
from .models import Legacy, Zone, Tribute, HistoricalPeriod, HistoricalEvent, Source, MediaItem


def _build_photo_url(obj, context):
    if not obj.photo:
        return None
    url = obj.photo.url
    if url.startswith("http"):
        return url
    r2_pub = os.environ.get("R2_PUBLIC_URL", "").rstrip("/")
    if r2_pub:
        if not r2_pub.startswith("http"):
            r2_pub = f"https://{r2_pub}"
        return f"{r2_pub}/{obj.photo.name}"
    request = context.get("request")
    if request:
        return request.build_absolute_uri(url)
    return url


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["id", "name", "slug"]


class HistoricalPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPeriod
        fields = ["id", "slug", "name", "years_label", "years_start", "years_end", "description", "order"]


class HistoricalEventSerializer(serializers.ModelSerializer):
    period_name = serializers.CharField(source="period.name", read_only=True)
    period_slug = serializers.CharField(source="period.slug", read_only=True)

    class Meta:
        model = HistoricalEvent
        fields = ["id", "slug", "name", "period_name", "period_slug", "event_date", "description"]


class SourceSerializer(serializers.ModelSerializer):
    source_type_display = serializers.CharField(source="get_source_type_display", read_only=True)

    class Meta:
        model = Source
        fields = [
            "id", "source_type", "source_type_display",
            "title", "url", "publication_date", "page_number", "excerpt",
        ]


class MediaItemSerializer(serializers.ModelSerializer):
    media_type_display = serializers.CharField(source="get_media_type_display", read_only=True)

    class Meta:
        model = MediaItem
        fields = [
            "id", "media_type", "media_type_display",
            "file", "external_url", "caption", "caption_om", "media_date", "order",
        ]


class LegacyListSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source="zone.name", read_only=True)
    photo_url = serializers.SerializerMethodField()
    story_preview = serializers.SerializerMethodField()
    period_name = serializers.CharField(source="historical_period.name", read_only=True)
    period_slug = serializers.CharField(source="historical_period.slug", read_only=True)

    class Meta:
        model = Legacy
        fields = [
            "id", "full_name", "occupation", "relationship_to_person",
            "slug", "zone_name", "photo_url", "story_preview",
            "birth_year", "death_year", "category", "gender",
            "period_name", "period_slug",
            "approved_at", "created_at",
        ]

    def get_story_preview(self, obj):
        if obj.story:
            return obj.story[:280]
        return ""

    def get_photo_url(self, obj):
        return _build_photo_url(obj, self.context)


class LegacyDetailSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source="zone.name", read_only=True)
    photo_url = serializers.SerializerMethodField()
    photo_enhanced_url = serializers.SerializerMethodField()
    historical_period = HistoricalPeriodSerializer(read_only=True)
    historical_event = HistoricalEventSerializer(read_only=True)
    sources = SourceSerializer(many=True, read_only=True)
    media_items = MediaItemSerializer(many=True, read_only=True)
    lifespan = serializers.CharField(read_only=True)

    class Meta:
        model = Legacy
        fields = [
            "id", "full_name", "alternative_spellings", "gender",
            "birth_year", "death_year", "date_of_death", "lifespan",
            "occupation", "category", "relationship_to_person",
            "slug", "zone_name", "woreda", "village",
            "place_of_death", "burial_location",
            "historical_period", "historical_event",
            "story", "story_en", "story_om", "original_language",
            "quote", "circumstances", "family_notes",
            "photo_url", "photo_enhanced_url", "photo_enhancement_status",
            "sources", "media_items",
            "verification_status", "approved_at", "created_at",
        ]

    def get_photo_url(self, obj):
        return _build_photo_url(obj, self.context)

    def get_photo_enhanced_url(self, obj):
        if not obj.photo_enhanced:
            return None
        url = obj.photo_enhanced.url
        if url.startswith("http"):
            return url
        r2_pub = os.environ.get("R2_PUBLIC_URL", "").rstrip("/")
        if r2_pub:
            if not r2_pub.startswith("http"):
                r2_pub = f"https://{r2_pub}"
            return f"{r2_pub}/{obj.photo_enhanced.name}"
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(url)
        return url


class LegacySubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legacy
        fields = [
            "full_name", "alternative_spellings", "gender",
            "birth_year", "death_year", "date_of_death",
            "occupation", "category", "relationship_to_person",
            "zone", "woreda", "village",
            "place_of_death", "burial_location",
            "historical_period", "historical_event",
            "story", "story_en", "story_om", "original_language",
            "circumstances", "family_notes",
            "photo",
        ]

    def validate(self, data):
        story_en = (data.get("story_en") or "").strip()
        story_om = (data.get("story_om") or "").strip()
        story = (data.get("story") or "").strip()
        if not story_en and not story_om and not story:
            raise serializers.ValidationError({"story_en": "Please provide the story in at least one language."})
        if story_en and not story:
            data["story"] = story_en
        elif story_om and not story:
            data["story"] = story_om
        if not story_en and story:
            data["story_en"] = story
        return data


class LegacyModerationSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source="zone.name", read_only=True)
    photo_url = serializers.SerializerMethodField()
    period_name = serializers.CharField(source="historical_period.name", read_only=True)

    class Meta:
        model = Legacy
        fields = [
            "id", "full_name", "occupation", "relationship_to_person",
            "slug", "zone_name", "photo_url",
            "story", "story_en", "story_om", "original_language",
            "birth_year", "death_year", "category",
            "period_name", "verification_status",
            "status", "created_at",
        ]

    def get_photo_url(self, obj):
        return _build_photo_url(obj, self.context)


class TributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribute
        fields = ["id", "tribute_type", "author_name", "message", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        if data.get("tribute_type") == Tribute.MESSAGE and not data.get("message", "").strip():
            raise serializers.ValidationError({"message": "A message tribute requires message text."})
        return data
