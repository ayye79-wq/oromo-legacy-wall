from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Legacy, ZoneModerator
from .forms import LegacySubmissionForm


# -------------------------
# Public views
# -------------------------
def home(request):
    q = (request.GET.get("q") or "").strip()

    qs = Legacy.objects.filter(status=Legacy.STATUS_APPROVED).order_by("-approved_at", "-created_at")

    # If you don't have these fields, remove them from the filter.
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q) |
            Q(story__icontains=q)
        )

    paginator = Paginator(qs, 24)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {
        "legacies": page_obj.object_list,
        "page_obj": page_obj,
        "q": q,
    })


def submit(request):
    if request.method == "POST":
        form = LegacySubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you. Your submission was received and will be reviewed before it appears publicly."
            )
            return redirect("home")
    else:
        form = LegacySubmissionForm()

    return render(request, "submit.html", {"form": form})


def legacy_detail(request, slug):
    legacy = get_object_or_404(Legacy, slug=slug, status=Legacy.STATUS_APPROVED)
    return render(request, "legacy_detail.html", {"legacy": legacy})


# -------------------------
# Moderation helpers
# -------------------------
def _moderator_zones(user):
    try:
        zm = ZoneModerator.objects.get(user=user)
        return zm.zones.all()
    except ZoneModerator.DoesNotExist:
        return []


# -------------------------
# Moderation views
# -------------------------
@login_required
def mod_queue(request):
    zones = _moderator_zones(request.user)
    if not zones:
        return HttpResponseForbidden("You are not assigned to any zone.")

    legacies = Legacy.objects.filter(
        status=Legacy.STATUS_PENDING,
        zone__in=zones,
    ).order_by("created_at")

    return render(request, "mod_queue.html", {"legacies": legacies})



@login_required
def mod_review(request, pk):
    zones = _moderator_zones(request.user)
    legacy = get_object_or_404(Legacy, pk=pk, status=Legacy.STATUS_PENDING)

    if legacy.zone not in zones:
        return HttpResponseForbidden("Not allowed.")

    return render(request, "mod_review.html", {"legacy": legacy})



@login_required
def mod_approve(request, pk):
    zones = _moderator_zones(request.user)
    legacy = get_object_or_404(Legacy, pk=pk, status=Legacy.STATUS_PENDING)

    if legacy.zone not in zones:
        return HttpResponseForbidden("Not allowed.")

    legacy.status = Legacy.STATUS_APPROVED
    legacy.approved_at = timezone.now()
    legacy.save(update_fields=["status", "approved_at"])

    return redirect("mod_queue")


@login_required
def mod_reject(request, pk):
    zones = _moderator_zones(request.user)
    legacy = get_object_or_404(Legacy, pk=pk, status=Legacy.STATUS_PENDING)

    if legacy.zone not in zones:
        return HttpResponseForbidden("Not allowed.")

    legacy.status = Legacy.STATUS_REJECTED
    legacy.save(update_fields=["status"])

    return redirect("mod_queue")
