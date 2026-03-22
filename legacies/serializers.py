from rest_framework import serializers
from .models import Legacy, Zone


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["id", "name", "slug"]


class LegacyListSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source="zone.name", read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Legacy
        fields = ["id", "full_name", "slug", "zone_name", "photo_url", "approved_at", "created_at"]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None


class LegacyDetailSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source="zone.name", read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Legacy
        fields = ["id", "full_name", "slug", "zone_name", "story", "photo_url", "approved_at", "created_at"]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None


class LegacySubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legacy
        fields = ["full_name", "zone", "story", "photo"]
