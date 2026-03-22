# Oromo Legacy Wall

A digital memorial platform for preserving and honoring the lives of Oromo individuals through stories, photos, and biographies. Community-driven with zone-based moderation.

## Architecture

**Full-stack:** React (Vite) frontend + Django REST API backend

- **Frontend:** React with Vite, running on port 5000
- **Backend:** Django REST Framework API, running on port 8000
- **Database:** SQLite (dev) / PostgreSQL-ready via psycopg
- **Image Handling:** Pillow + WhiteNoise
- **Production Server:** Gunicorn

## Project Structure

```
/
├── oromolegacy/          # Django project config (settings, urls, wsgi)
├── legacies/             # Core Django app
│   ├── models.py         # Zone, ZoneModerator, Legacy
│   ├── serializers.py    # DRF serializers
│   ├── api_views.py      # REST API views
│   ├── views.py          # Moderation dashboard views
│   └── urls.py           # URL routing
├── frontend/             # React (Vite) frontend
│   └── src/
│       ├── App.jsx       # Router + layout
│       ├── api.js        # API utility
│       ├── components/   # Navbar, Footer, LegacyCard
│       └── pages/        # Home, SubmitLegacy, LegacyDetail
├── static/               # Django source static files
├── staticfiles/          # Collected static files
├── legacy_photos/        # Uploaded memorial photos (MEDIA_ROOT)
├── db.sqlite3            # SQLite database
├── requirements.txt      # Python dependencies
└── start.sh              # Production startup script
```

## Key Models

- **Zone** — Geographic/administrative zones of Oromiyaa
- **ZoneModerator** — Links Django users to the zones they moderate
- **Legacy** — Memorial entries (pending/approved/rejected)

## API Endpoints

- `GET /api/zones/` — List all zones
- `GET /api/legacies/` — List approved legacies (search: `?q=`, `?zone=`)
- `GET /api/legacies/<slug>/` — Get a specific legacy
- `POST /api/legacies/submit/` — Submit a new legacy (multipart)

## Development

```bash
# Start Django API (port 8000)
python manage.py runserver 0.0.0.0:8000

# Start React frontend (port 5000)
cd frontend && npm run dev
```

The Vite dev server proxies `/api` and `/media` requests to Django on port 8000.

## Production Deployment

Build step: `cd frontend && npm install && npm run build && cd .. && python manage.py collectstatic --noinput`

Run command: `gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=2 oromolegacy.wsgi:application`

Django serves the React build via a catch-all view when deployed.

## Moderation

- Zone moderators log in at `/admin/` and access `/moderation/queue/`
- Submissions are pending by default and only appear on the wall after approval
- Each moderator is assigned to one or more zones

## Settings Notes

- `ALLOWED_HOSTS` includes all Replit domains
- `CSRF_TRUSTED_ORIGINS` configured for Replit proxy
- `CORS_ALLOW_ALL_ORIGINS = True` for development
- `MEDIA_ROOT` = `legacy_photos/`
- `STATIC_ROOT` = `staticfiles/`
