# Oromo Legacy Wall

A digital memorial platform for preserving and honoring the lives of Oromo individuals through stories, photos, and biographies. Community-driven with zone-based moderation.

## Architecture

**Full-stack:** React (Vite) frontend + Django REST API backend + Expo React Native mobile app

- **Frontend:** React with Vite, running on port 5000
- **Backend:** Django REST Framework API, running on port 8000
- **Database:** PostgreSQL (via Replit's built-in DB, using DATABASE_URL secret)
- **Mobile:** Expo React Native app with expo-router, running on port 8080
- **Image Handling:** Pillow + WhiteNoise
- **Production Server:** Gunicorn

## Design Language

- **Background:** Warm charcoal `#0e0a06` (black with brown undertone)
- **Accent:** Amber candlelight `#c9923a` / `#ddb06a`
- **Text:** Cream `#f0e6d0` (primary), `#b8956a` (secondary)
- **Fonts:** EB Garamond + Cormorant Garamond (web), system fonts (mobile)
- **Tone:** Reverent, memorial — "Honor a Life", "Wall of Remembrance", "Read Their Story →"

## Project Structure

```
/
├── oromolegacy/          # Django project config (settings, urls, wsgi)
├── legacies/             # Core Django app
│   ├── models.py         # Zone, ZoneModerator, Legacy (+ 5 PostgreSQL indexes)
│   ├── serializers.py    # DRF serializers
│   ├── api_views.py      # REST API views (with select_related for N+1 prevention)
│   ├── views.py          # Moderation dashboard views
│   └── urls.py           # URL routing
├── frontend/             # React (Vite) frontend
│   └── src/
│       ├── App.jsx       # Router + layout
│       ├── api.js        # API utility
│       ├── components/   # Navbar, Footer, LegacyCard
│       └── pages/        # Home, SubmitLegacy, LegacyDetail
├── mobile/               # Expo React Native mobile app
│   ├── app/
│   │   ├── _layout.tsx           # Root layout (QueryClient, SafeAreaProvider)
│   │   ├── (tabs)/_layout.tsx    # Tab navigation (Wall, Honor a Life)
│   │   ├── (tabs)/index.tsx      # Memorial Wall (search, zone filter, list)
│   │   ├── (tabs)/honor.tsx      # Honor a Life form (photo picker)
│   │   └── legacy/[slug].tsx     # Legacy detail screen
│   ├── lib/api.ts                # API functions (EXPO_PUBLIC_API_URL)
│   ├── app.json                  # Expo config
│   └── package.json
├── legacy_photos/        # Uploaded memorial photos (MEDIA_ROOT)
├── requirements.txt      # Python dependencies
└── start.sh              # Production startup script
```

## Key Models

- **Zone** — Geographic/administrative zones of Oromiyaa (22 zones seeded)
- **ZoneModerator** — Links Django users to the zones they moderate
- **Legacy** — Memorial entries with `story_en`, `story_om`, `original_language` fields; pending/approved/rejected status; 5 PostgreSQL indexes
- **Tribute** — Candles and messages left on individual legacy pages

## Bilingual System (EN + Afaan Oromo)

- Language toggle `EN | AO` in navbar — persisted in localStorage
- All UI strings translated: `frontend/src/i18n/translations.js`
- Language context: `frontend/src/i18n/LanguageContext.jsx` — `useLang()` hook returns `{ lang, setLang, t }`
- Story display logic on detail page:
  - Toggle = OM: show `story_om` if present, else fallback to `story_en` + note
  - Toggle = EN: show `story_en` if present, else show original language story
- Submission form: choose "Write in English", "Write in Afaan Oromo", or "Write in Both"
- No auto-translation ever — all story content is human-authored
- `original_language` field records which language a story was written in

## API Endpoints

- `GET /api/zones/` — List all zones
- `GET /api/legacies/` — List approved legacies (search: `?q=`, `?zone=`)
- `GET /api/legacies/<slug>/` — Get a specific legacy (includes `story_en`, `story_om`, `original_language`)
- `POST /api/submit/` — Submit a new legacy (multipart, accepts `story_en`, `story_om`, `original_language`)
- `GET /api/legacies/<slug>/tributes/` — List tributes (candle count + messages)
- `POST /api/legacies/<slug>/tributes/` — Light a candle or leave a message

## Environment Variables

- `DATABASE_URL` — PostgreSQL connection string (Replit secret, auto-provided)
- `EXPO_PUBLIC_API_URL` — Django API base URL for mobile app (set to main Replit dev domain)

## Development

```bash
# Django API (port 8000) — workflow: "Django API"
python manage.py runserver 0.0.0.0:8000

# React frontend (port 5000) — workflow: "Start application"
cd frontend && npm run dev

# Expo mobile app (port 8080) — workflow: "Expo Mobile"
cd mobile && npx expo start --web --port 8080
```

The Vite dev server proxies `/api` and `/media` requests to Django on port 8000.
The Expo mobile app calls the API via `EXPO_PUBLIC_API_URL` (set to the Vite dev server URL).

## Database

- **Engine:** PostgreSQL (via `dj-database-url` + `psycopg2-binary`)
- **Fallback:** SQLite if `DATABASE_URL` not set
- **Indexes:** `legacy_status_idx`, `legacy_status_approved_idx`, `legacy_zone_status_idx`, `legacy_created_idx`, `legacy_approved_idx`
- All 22 Oromiyaa zones and existing legacies are seeded in PostgreSQL

## Production Deployment

Build step: `cd frontend && npm install && npm run build && cd .. && python manage.py collectstatic --noinput`

Run command: `gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=2 oromolegacy.wsgi:application`

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
