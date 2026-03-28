from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, HttpResponse, JsonResponse
from pathlib import Path


def serve_react(request, *args, **kwargs):
    index = Path(settings.BASE_DIR) / "frontend" / "dist" / "index.html"
    if index.exists():
        return FileResponse(open(index, "rb"), content_type="text/html")
    return HttpResponse("Frontend not built. Run: cd frontend && npm run build", status=503)


def ping(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("ping/", ping, name="ping"),
    path("admin/", admin.site.urls),
    path("", include("legacies.urls")),
    re_path(r"^(?!api/|admin/|static/|media/).*$", serve_react),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
