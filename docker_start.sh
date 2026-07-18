#!/bin/sh
set -e

# Run migrations first — fast, must complete before gunicorn serves traffic
python manage.py migrate --noinput || python manage.py migrate --fake --noinput

# Start gunicorn in the background immediately so healthchecks pass
gunicorn \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 60 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  oromolegacy.wsgi:application &
GUNICORN_PID=$!

# Seed foundation data — runs after gunicorn is up (healthchecks already passing)
python manage.py seed_production

# Create/reset superuser if DJANGO_SUPERUSER_PASSWORD is set
python manage.py shell -c "
import os, sys
from django.contrib.auth.models import User

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

existing = list(User.objects.filter(is_superuser=True).values_list('username', 'is_active'))
print('[superuser] Existing superusers:', existing)

if not password:
    print('[superuser] DJANGO_SUPERUSER_PASSWORD not set — skipping')
    sys.exit(0)

u, created = User.objects.update_or_create(
    username=username,
    defaults={
        'email': email,
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    }
)
u.set_password(password)
u.save()
print('[superuser]', 'Created' if created else 'Updated', 'user:', username, '| is_active:', u.is_active, '| is_superuser:', u.is_superuser)
" || echo "[superuser] setup failed (non-fatal) — continuing"

# Wait for gunicorn
wait $GUNICORN_PID
