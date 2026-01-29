from django.urls import path
from . import views

urlpatterns = [
    # public
    path("", views.home, name="home"),
    path("submit/", views.submit, name="submit"),
    path("legacy/<slug:slug>/", views.legacy_detail, name="legacy_detail"),

    # moderation (custom dashboard)
    path("moderation/queue/", views.mod_queue, name="mod_queue"),
    path("moderation/review/<int:pk>/", views.mod_review, name="mod_review"),
    path("moderation/approve/<int:pk>/", views.mod_approve, name="mod_approve"),
    path("moderation/reject/<int:pk>/", views.mod_reject, name="mod_reject"),
]
