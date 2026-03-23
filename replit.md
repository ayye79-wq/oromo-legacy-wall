# Oromo Legacy Wall

A digital memorial platform for preserving and honoring the lives of Oromo individuals through stories, photos, and biographies. Community-driven with zone-based moderation.

## Architecture

**Full-stack:** React (Vite) frontend + Django REST API backend + Expo React Native mobile app

- **Frontend:** React with Vite, running on port 5000
- **Backend:** Django REST Framework API, running on port 8000
- **Database:** PostgreSQL (via Replit's built-in DB, using DATABASE_URL secret)
- **Mobile:** Expo React Native app with expo-router, running on port 8080
- **Image Handling:** Pillow (auto-compress + WebP-quality JPEG on upload) + WhiteNoise
- **Production Server:** Gunicorn

## Design Language

- **Background:** Dark navy `#0b1220` → `#0a0f1a` gradient
- **Gold palette:** `--gold-primary: #d4af37` (headings/buttons), `--gold-soft: #caa85a` (dividers), `--gold-muted: #a88f3a` (tags)
- **Text:** `--text-primary: #f5f5f5` (titles), `--text-secondary: #cfcfcf` (body)
- **Card borders:** `rgba(212,175,55,0.15)` subtle gold
- **Odaa tree icon:** `#5c9e4c`
- **Fonts:** Cormorant Garamond + EB Garamond (web), system fonts (mobile)
- **Tone:** Reverent, memorial — "Honor a Life", "Wall of Remembrance", "Read Their Story →"

## Project Structure

```
/
├── oromolegacy/          # Django project config (settings, urls, wsgi)
├── legacies/             # Core Django app
│   ├── models.py         # Zone, ZoneModerator, Legacy, Tribute (+ image compression)
│   ├── serializers.py    # DRF serializers (incl. LegacyModerationSerializer)
│   ├── api_views.py      # REST API views
│   ├── signals.py        # Email notification on new submission
│   ├── views.py          # Moderation dashboard views
│   └── urls.py           # URL routing
├── frontend/             # React (Vite) frontend
│   └── src/
│       ├── App.jsx       # Router + layout (HelmetProvider)
│       ├── api.js        # API utility
│       ├── components/   # Navbar, Footer, LegacyCard, TributeSection
│       └── pages/
│           ├── Home.jsx         # Wall + hero counter + skeleton loading
│           ├── LegacyDetail.jsx # Detail + OG meta tags + lightbox
│           ├── SubmitLegacy.jsx # Form + char picker + relationship field + honeypot
│           └── Moderation.jsx   # Moderation dashboard (password-protected)
├── mobile/               # Expo React Native mobile app
│   ├── app/
│   │   ├── _layout.tsx
│   │   ├── (tabs)/_layout.tsx
│   │   ├── (tabs)/index.tsx
│   │   ├── (tabs)/honor.tsx
│   │   └── legacy/[slug].tsx
│   ├── lib/api.ts
│   └── lib/lang.ts
├── legacy_photos/        # Uploaded memorial photos (MEDIA_ROOT)
├── requirements.txt
└── start.sh
```

## Key Models

- **Zone** — Geographic/administrative zones of Oromiyaa (22 zones seeded)
- **ZoneModerator** — Links Django users to zones they moderate
- **Legacy** — Memorial entries: `story_en`, `story_om`, `original_language`, `relationship_to_person`; pending/approved/rejected status; 5 PostgreSQL indexes; auto-compresses photos to JPEG on upload
- **Tribute** — Candles and messages left on individual legacy pages

## Bilingual System (EN + Afaan Oromo)

- Language toggle `EN | AO` in navbar — persisted in localStorage
- All UI strings translated: `frontend/src/i18n/translations.js`
- Language context: `frontend/src/i18n/LanguageContext.jsx` — `useLang()` hook
- Submission form: choose "Write in English", "Write in Afaan Oromo", or "Write in Both"
- Afaan Oromo special character picker in story textarea (apostrophe, digraphs, long vowels)
- No auto-translation ever — all story content is human-authored

## API Endpoints

- `GET /api/zones/` — List all zones
- `GET /api/count/` — Count of approved legacies `{"approved": N}`
- `GET /api/legacies/` — List approved legacies (search: `?q=`, `?zone=`)
- `GET /api/legacies/<slug>/` — Get a specific legacy
- `POST /api/legacies/submit/` — Submit a new legacy (multipart; honeypot field `website`)
- `GET /api/legacies/<slug>/tributes/` — List tributes
- `POST /api/legacies/<slug>/tributes/` — Light a candle or leave a message
- `GET /api/mod/pending/` — List pending submissions (requires Bearer token = MOD_SECRET)
- `POST /api/mod/<id>/approve/` — Approve a submission (requires Bearer token)
- `POST /api/mod/<id>/reject/` — Reject a submission (requires Bearer token)

## Environment Variables

- `DATABASE_URL` — PostgreSQL connection string (Replit secret, auto-provided)
- `EXPO_PUBLIC_API_URL` — Django API base URL for mobile app
- `MOD_SECRET` — Password for the `/mod` moderation dashboard (default: `oromo-mod-2024` — **change in production**)
- `ADMIN_NOTIFICATION_EMAIL` — Email to notify on new submission
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` — SMTP config
- `DEFAULT_FROM_EMAIL` — Sender address for notification emails

## Frontend Features

1. **Hero counter** — Live "X lives honored on this wall" pulled from `/api/count/`
2. **Skeleton loading** — Shimmer placeholder cards while wall loads (no spinner)
3. **Open Graph meta tags** — Per-legacy `og:title`, `og:description`, `og:image` via react-helmet-async
4. **Photo lightbox** — Click portrait to expand full-screen; close with Escape or ✕
5. **Afaan Oromo char picker** — Inline button bar above Afaan Oromo textarea (inserts at cursor)
6. **Relationship to person** — Optional field in submit form, shown in sidebar on detail page
7. **Honeypot spam protection** — Hidden `website` field; if filled = silent discard
8. **Moderation dashboard** — `/mod` page with password login, card view, approve/reject

## Moderation Dashboard

- URL: `/mod`
- Default password: `oromo-mod-2024` (set `MOD_SECRET` env var to change)
- Password stored in sessionStorage — auto-expires when tab closes
- Shows all pending submissions with photo, story, relationship, zone
- Approve/Reject buttons update status instantly; success toast confirmation
- Also accessible via Django admin at `/admin/` (requires login) → legacy list

## Image Compression

Photos are automatically compressed on upload:
- Resized to max 800×1000px
- Saved as JPEG at 82% quality with optimization
- Original file replaced; new name: `legacy_photos/<slug>.jpg`
- Never fails silently — if compression errors, original is kept

## Development

```bash
# Django API (port 8000)
python manage.py runserver 0.0.0.0:8000

# React frontend (port 5000)
cd frontend && npm run dev

# Expo mobile (port 8080)
cd mobile && npx expo start --web --port 8080
```

The Vite dev server proxies `/api` and `/media` to Django on port 8000.

## Database

- **Engine:** PostgreSQL (via `dj-database-url`)
- **Fallback:** SQLite if `DATABASE_URL` not set
- **Migrations:** 0001 through 0007 (latest adds `relationship_to_person`)

## Production Deployment

Build step: `cd frontend && npm install && npm run build && cd .. && python manage.py collectstatic --noinput`

Run command: `gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=2 oromolegacy.wsgi:application`

## Settings Notes

- `ALLOWED_HOSTS` includes all Replit domains
- `CSRF_TRUSTED_ORIGINS` configured for Replit proxy
- `CORS_ALLOW_ALL_ORIGINS = True`
- API views that accept public submissions use `authentication_classes = []` and `permission_classes = [AllowAny]`
- Moderation API verified via `Authorization: Bearer <MOD_SECRET>` header
