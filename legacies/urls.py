from django.urls import path
from . import views, api_views

urlpatterns = [
    path("api/zones/", api_views.ZoneListView.as_view(), name="api-zones"),
    path("api/legacies/submit/", api_views.LegacySubmitView.as_view(), name="api-submit"),
    path("api/legacies/<slug:slug>/", api_views.LegacyDetailView.as_view(), name="api-legacy-detail"),
    path("api/legacies/", api_views.LegacyListView.as_view(), name="api-legacies"),

    path("moderation/queue/", views.mod_queue, name="mod_queue"),
    path("moderation/review/<int:pk>/", views.mod_review, name="mod_review"),
    path("moderation/approve/<int:pk>/", views.mod_approve, name="mod_approve"),
    path("moderation/reject/<int:pk>/", views.mod_reject, name="mod_reject"),
]
