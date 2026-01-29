from .models import ZoneModerator

def is_admin(user) -> bool:
    return bool(user and user.is_authenticated and user.is_superuser)

def is_zone_mod(user) -> bool:
    return bool(user and user.is_authenticated and ZoneModerator.objects.filter(user=user).exists())
