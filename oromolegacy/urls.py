from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from django.utils import timezone
from pathlib import Path


def serve_react(request, *args, **kwargs):
    index = Path(settings.BASE_DIR) / "frontend" / "dist" / "index.html"
    if index.exists():
        return FileResponse(open(index, "rb"), content_type="text/html")
    return HttpResponse("Frontend not built. Run: cd frontend && npm run build", status=503)


def ping(request):
    return JsonResponse({"status": "ok"})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /api/",
        "Disallow: /admin/",
        "Disallow: /moderation/",
        "",
        "Sitemap: https://oromolegacywall.org/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    from legacies.models import Legacy
    base = "https://oromolegacywall.org"
    today = timezone.now().date().isoformat()

    heroes = Legacy.objects.filter(status=Legacy.STATUS_APPROVED).only("slug", "approved_at")

    urls = [
        f"""  <url>
    <loc>{base}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <lastmod>{today}</lastmod>
  </url>""",
        f"""  <url>
    <loc>{base}/about</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <lastmod>{today}</lastmod>
  </url>""",
        f"""  <url>
    <loc>{base}/submit</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
    <lastmod>{today}</lastmod>
  </url>""",
    ]

    for hero in heroes:
        lastmod = hero.approved_at.date().isoformat() if hero.approved_at else today
        urls.append(f"""  <url>
    <loc>{base}/legacy/{hero.slug}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
    <lastmod>{lastmod}</lastmod>
  </url>""")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(urls)
    xml += "\n</urlset>"
    return HttpResponse(xml, content_type="application/xml")


urlpatterns = [
    path("ping/", ping, name="ping"),
    path("robots.txt", robots_txt, name="robots-txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap-xml"),
    path("admin/", admin.site.urls),
    path("", include("legacies.urls")),
    re_path(r"^(?!api/|admin/|static/|media/).*$", serve_react),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
