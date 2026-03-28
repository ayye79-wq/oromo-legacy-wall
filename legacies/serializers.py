import os
from rest_framework import serializers
from .models import Legacy, Zone, Tribute


def _build_photo_url(obj, context):
    """
    Return an absolute URL for the hero's photo.
    Priority:
      1. If DEFAULT_FILE_STORAGE is R2, obj.photo.url is already absolute → use it.
      2. Else fall back to R2_PUBLIC_URL env var (files live in R2 even if Django
         isn't using it as default storage).
      3. Else build absolute URL from the current request.
    """
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


class LegacyListSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source="zone.name", read_only=True)
    photo_url = serializers.SerializerMethodField()
    story_preview = serializers.SerializerMethodField()

    class Meta:
        model = Legacy
        fields = [
            "id", "full_name", "occupation", "relationship_to_person",
            "slug", "zone_name", "photo_url", "story_preview",
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

    class Meta:
        model = Legacy
        fields = [
            "id", "full_name", "occupation", "relationship_to_person",
            "slug", "zone_name",
            "story", "story_en", "story_om", "original_language",
            "photo_url", "approved_at", "created_at",
        ]

    def get_photo_url(self, obj):
        return _build_photo_url(obj, self.context)


class LegacySubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legacy
        fields = [
            "full_name", "occupation", "relationship_to_person",
            "zone", "story", "story_en", "story_om", "original_language", "photo",
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

    class Meta:
        model = Legacy
        fields = [
            "id", "full_name", "occupation", "relationship_to_person",
            "slug", "zone_name", "photo_url",
            "story", "story_en", "story_om", "original_language",
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
