from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Legacy, Zone, Tribute
from .serializers import (
    ZoneSerializer,
    LegacyListSerializer,
    LegacyDetailSerializer,
    LegacySubmitSerializer,
    LegacyModerationSerializer,
    TributeSerializer,
)


def _check_mod_auth(request):
    mod_secret = getattr(settings, 'MOD_SECRET', '')
    if not mod_secret:
        return False
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        token = auth[7:]
        return token == mod_secret
    return False


class ZoneListView(generics.ListAPIView):
    queryset = Zone.objects.all().order_by("name")
    serializer_class = ZoneSerializer


class LegacyListView(generics.ListAPIView):
    serializer_class = LegacyListSerializer

    def get_queryset(self):
        qs = (
            Legacy.objects
            .filter(status=Legacy.STATUS_APPROVED)
            .select_related("zone")
            .order_by("-approved_at", "-created_at")
        )
        q = self.request.query_params.get("q", "").strip()
        zone = self.request.query_params.get("zone", "").strip()
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(story__icontains=q))
        if zone:
            qs = qs.filter(zone__slug=zone)
        return qs

    def get_serializer_context(self):
        return {"request": self.request}


class LegacyCountView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        count = Legacy.objects.filter(status=Legacy.STATUS_APPROVED).count()
        return Response({"approved": count})


class LegacyDetailView(generics.RetrieveAPIView):
    serializer_class = LegacyDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Legacy.objects
            .filter(status=Legacy.STATUS_APPROVED)
            .select_related("zone")
        )

    def get_serializer_context(self):
        return {"request": self.request}


class LegacySubmitView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        if request.data.get('website', '').strip():
            return Response(
                {"message": "Thank you. Your submission was received and will be reviewed before it appears publicly."},
                status=status.HTTP_201_CREATED,
            )

        serializer = LegacySubmitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Thank you. Your submission was received and will be reviewed before it appears publicly."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TributeListCreateView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, slug):
        legacy = get_object_or_404(Legacy, slug=slug, status=Legacy.STATUS_APPROVED)
        tributes = legacy.tributes.all()
        candle_count = tributes.filter(tribute_type=Tribute.CANDLE).count()
        messages_qs = tributes.filter(tribute_type=Tribute.MESSAGE)
        serializer = TributeSerializer(messages_qs, many=True)
        return Response({
            "candle_count": candle_count,
            "message_count": messages_qs.count(),
            "messages": serializer.data,
        })

    def post(self, request, slug):
        legacy = get_object_or_404(Legacy, slug=slug, status=Legacy.STATUS_APPROVED)
        serializer = TributeSerializer(data=request.data)
        if serializer.is_valid():
            tribute = serializer.save(legacy=legacy)
            candle_count = legacy.tributes.filter(tribute_type=Tribute.CANDLE).count()
            return Response({
                "tribute": TributeSerializer(tribute).data,
                "candle_count": candle_count,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModPendingView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        if not _check_mod_auth(request):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        legacies = (
            Legacy.objects
            .filter(status=Legacy.STATUS_PENDING)
            .select_related("zone")
            .order_by("created_at")
        )
        serializer = LegacyModerationSerializer(legacies, many=True)
        return Response({"results": serializer.data, "count": legacies.count()})


class ModApproveView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not _check_mod_auth(request):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        legacy = get_object_or_404(Legacy, pk=pk)
        legacy.status = Legacy.STATUS_APPROVED
        legacy.approved_at = timezone.now()
        legacy.save(update_fields=["status", "approved_at"])
        return Response({"ok": True, "status": "APPROVED"})


class ModRejectView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, pk):
        if not _check_mod_auth(request):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        legacy = get_object_or_404(Legacy, pk=pk)
        legacy.status = Legacy.STATUS_REJECTED
        legacy.save(update_fields=["status"])
        return Response({"ok": True, "status": "REJECTED"})
