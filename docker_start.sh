#!/bin/sh
set -e

# Run migrations
python manage.py migrate --noinput 2>&1 | head -30

# Create/reset superuser if DJANGO_SUPERUSER_PASSWORD is set
python manage.py shell -c "
import os, sys
from django.contrib.auth.models import User
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
if not password:
    print('[superuser] DJANGO_SUPERUSER_PASSWORD not set — skipping')
    sys.exit(0)
u, created = User.objects.get_or_create(username=username)
u.email       = email
u.is_staff    = True
u.is_superuser = True
u.set_password(password)
u.save()
print('[superuser]', 'Created' if created else 'Updated', 'admin user:', username)
" || echo "[superuser] setup step failed (non-fatal) — continuing"

# Start gunicorn – PORT is injected by Railway
exec gunicorn \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 60 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  oromolegacy.wsgi:application
