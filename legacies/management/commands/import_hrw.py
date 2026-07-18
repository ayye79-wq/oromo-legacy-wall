"""
Management command: import_hrw

Imports the HRW 314-name list from an Excel file into the Legacy model.

Usage:
    python manage.py import_hrw <path_to_xlsx> [--dry-run] [--status PENDING]

The command:
  - Maps source zones to existing Zone objects
  - Sets historical_period to 'protests-2014-2018'
  - Sets historical_event to 'addis-ababa-master-plan-protests' (Oromo protests era)
  - Sets verification_status='partial' (one credible source)
  - Sets category='civilian' as default (can be updated in admin)
  - Creates a Source record for each entry (HRW report)
  - Skips rows whose full_name already exists in the DB (duplicate check)
  - Reports a full summary at the end
"""
import re
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from legacies.models import Legacy, Zone, HistoricalPeriod, HistoricalEvent, Source


# ── Zone mapping: source zone label → Zone slug ──────────────────────────────
SOURCE_ZONE_MAP = {
    'West Shewa': 'west-shewa',
    'SW Shewa': 'south-west-shewa',
    'S.W. Shewa': 'south-west-shewa',
    'North Shewa': 'north-shewa-oromia',
    'East Hararghe': 'east-hararghe',
    'West Hararghe': 'west-hararghe',
    'West Arsi': 'west-arsi',
    'West Wollega': 'west-wollega',
    'East Wollega': 'east-wollega',
    'Horo Gudru Wollega': 'horo-guduru-wollega',
    'Horo Gudru, Wollega': 'horo-guduru-wollega',
    'Kelem Wollega': 'kelem-wollega',
    'Guji': 'guji',
    'Borana': 'borana',
    'Borena': 'borena',
    'Bale': 'bale',
    'Arsi': 'arsi',
    # Outside Oromia — map to closest fallback
    'SNNPR': 'shewa',
    'Dire Dawa': 'east-hararghe',
    'Addis Ababa': 'shewa',
}

# Broad zone column → Zone slug (fallback when source zone is '-' or missing)
BROAD_ZONE_MAP = {
    'Arsi': 'arsi',
    'Bale': 'bale',
    'Borana': 'borana',
    'Guji': 'guji',
    'Hararghe': 'east-hararghe',
    'Shewa': 'shewa',
    'Wollega': 'west-wollega',
    'Outside Oromia / Needs Review': 'shewa',
    'Unknown / Needs Review': 'shewa',
}

HRW_SOURCE_TYPE = 'hrw'
HRW_SOURCE_TITLE = '"Such a Brutal Crackdown": Killings and Arrests in Response to Ethiopia\'s Oromo Protests'
HRW_SOURCE_URL = 'https://www.hrw.org/sites/default/files/report_pdf/ethiopia0616web.pdf'


def _parse_date(raw):
    """Try to extract a year from date strings like '1-Dec-2015', '2/3-Dec-2015'."""
    if not raw or raw == '-':
        return None, None
    raw = str(raw).strip()
    # Find a 4-digit year
    m = re.search(r'(\d{4})', raw)
    year = int(m.group(1)) if m else None
    # Try to parse a full date
    for fmt in ('%d-%b-%Y', '%d/%m/%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(raw, fmt).date(), year
        except ValueError:
            pass
    # Try first portion if range like "2/3-Dec-2015"
    cleaned = re.sub(r'^\d+/', '', raw)  # strip "2/" from "2/3-Dec-2015"
    for fmt in ('%d-%b-%Y',):
        try:
            return datetime.strptime(cleaned, fmt).date(), year
        except ValueError:
            pass
    return None, year


def _unique_slug(base_slug):
    slug = base_slug[:200]
    if not Legacy.objects.filter(slug=slug).exists():
        return slug
    for i in range(2, 9999):
        candidate = f"{base_slug[:196]}-{i}"
        if not Legacy.objects.filter(slug=candidate).exists():
            return candidate
    return f"{base_slug[:190]}-{datetime.now().timestamp():.0f}"


class Command(BaseCommand):
    help = 'Import HRW 314-name list from Excel into Legacy records'

    def add_arguments(self, parser):
        parser.add_argument('xlsx_path', type=str, help='Path to the .xlsx file')
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Parse and report without writing to the database'
        )
        parser.add_argument(
            '--status', type=str, default='PENDING',
            choices=['PENDING', 'APPROVED'],
            help='Status to assign imported records (default: PENDING)'
        )

    def handle(self, *args, **options):
        try:
            import openpyxl
        except ImportError:
            raise CommandError('openpyxl is required: pip install openpyxl')

        xlsx_path = options['xlsx_path']
        dry_run = options['dry_run']
        import_status = options['status']

        self.stdout.write(f'\n{"DRY RUN — " if dry_run else ""}Importing HRW list from: {xlsx_path}\n')

        # Load workbook
        try:
            wb = openpyxl.load_workbook(xlsx_path)
        except Exception as e:
            raise CommandError(f'Could not open file: {e}')

        ws = wb.active

        # Pre-load Zone lookup table
        zone_by_slug = {z.slug: z for z in Zone.objects.all()}

        def get_zone(source_zone_raw, broad_zone_raw):
            sz = (source_zone_raw or '').strip()
            bz = (broad_zone_raw or '').strip()
            if sz and sz != '-':
                slug = SOURCE_ZONE_MAP.get(sz)
                if slug and slug in zone_by_slug:
                    return zone_by_slug[slug]
            # Fallback to broad zone
            slug = BROAD_ZONE_MAP.get(bz)
            if slug and slug in zone_by_slug:
                return zone_by_slug[slug]
            # Last resort: shewa
            return zone_by_slug.get('shewa') or zone_by_slug.get('west-shewa')

        # Load period and event
        try:
            period = HistoricalPeriod.objects.get(slug='protests-2014-2018')
        except HistoricalPeriod.DoesNotExist:
            period = None
            self.stdout.write(self.style.WARNING('  Warning: period "protests-2014-2018" not found'))

        try:
            event = HistoricalEvent.objects.get(slug='addis-ababa-master-plan-protests')
        except HistoricalEvent.DoesNotExist:
            event = None

        # Existing names for duplicate detection
        existing_names = set(
            Legacy.objects.values_list('full_name', flat=True)
        )
        existing_slugs = set(
            Legacy.objects.values_list('slug', flat=True)
        )

        # ── Process rows (data starts at row 5) ──
        created = 0
        skipped_dup = 0
        skipped_empty = 0
        zone_fallbacks = []
        errors = []

        rows = list(ws.iter_rows(min_row=5, values_only=True))

        for i, row in enumerate(rows, start=5):
            record_num = row[0]
            full_name = (row[1] or '').strip()
            occupation = (row[2] or '').strip()
            relationship = (row[3] or '').strip()
            broad_zone_raw = (row[4] or '').strip()
            story = (row[6] or '').strip()
            source_zone_raw = (row[8] or '').strip()
            date_raw = row[9]
            source_title = (row[10] or HRW_SOURCE_TITLE).strip()
            source_url = (row[11] or HRW_SOURCE_URL).strip()

            if not full_name:
                skipped_empty += 1
                continue

            # Duplicate check
            if full_name in existing_names:
                skipped_dup += 1
                self.stdout.write(f'  SKIP (duplicate): {full_name}')
                continue

            # Zone resolution
            zone = get_zone(source_zone_raw, broad_zone_raw)
            if not zone:
                errors.append(f'Row {i}: No zone found for "{full_name}" (source_zone={source_zone_raw!r}, broad={broad_zone_raw!r})')
                continue
            # Flag if we used fallback
            if source_zone_raw and source_zone_raw != '-' and source_zone_raw not in SOURCE_ZONE_MAP:
                zone_fallbacks.append(f'  Row {i}: unmapped source_zone {source_zone_raw!r} → used broad zone "{broad_zone_raw}"')

            # Parse date
            date_of_death, death_year = _parse_date(date_raw)

            # Build slug
            base_slug = slugify(full_name)[:200] or f'hrw-{record_num}'
            slug = _unique_slug(base_slug)

            if dry_run:
                self.stdout.write(
                    f'  [{record_num:3d}] {full_name} | zone={zone.slug} | '
                    f'death={date_of_death} | slug={slug}'
                )
                created += 1
                existing_names.add(full_name)
                continue

            # Create Legacy
            try:
                legacy = Legacy(
                    full_name=full_name,
                    slug=slug,
                    occupation=occupation,
                    relationship_to_person=relationship or 'Historical record / HRW source',
                    zone=zone,
                    story=story,
                    story_en=story,
                    original_language='en',
                    category='civilian',
                    historical_period=period,
                    historical_event=event,
                    death_year=death_year,
                    date_of_death=date_of_death,
                    place_of_death=source_zone_raw if source_zone_raw and source_zone_raw != '-' else '',
                    verification_status='partial',
                    notes='Imported from HRW Annex 1. Needs family/community verification before approval.',
                    status=import_status,
                )
                # Skip photo compression trigger — no photo
                Legacy.objects.bulk_create([legacy])
                # Re-fetch for FK creation
                legacy = Legacy.objects.get(slug=slug)

                Source.objects.create(
                    legacy=legacy,
                    source_type=HRW_SOURCE_TYPE,
                    title=source_title,
                    url=source_url,
                    publication_date='2016-06-15',
                    excerpt=f'Listed in Annex 1 — Partial List of Alleged Victims of Killings. '
                            f'Date of death: {date_raw}. Location: {source_zone_raw}.',
                )

                created += 1
                existing_names.add(full_name)
                self.stdout.write(f'  ✓ [{record_num:3d}] {full_name} ({zone.slug})')

            except Exception as e:
                errors.append(f'Row {i} — {full_name}: {e}')

        # ── Summary ──
        self.stdout.write('\n' + '─' * 60)
        self.stdout.write(self.style.SUCCESS(f'  Created:          {created}'))
        self.stdout.write(f'  Skipped (dup):    {skipped_dup}')
        self.stdout.write(f'  Skipped (empty):  {skipped_empty}')
        if zone_fallbacks:
            self.stdout.write(self.style.WARNING(f'\n  Zone fallbacks ({len(zone_fallbacks)}):'))
            for zf in zone_fallbacks:
                self.stdout.write(zf)
        if errors:
            self.stdout.write(self.style.ERROR(f'\n  Errors ({len(errors)}):'))
            for err in errors:
                self.stdout.write(f'  ✗ {err}')
        self.stdout.write('─' * 60 + '\n')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN complete — nothing written to database.\n'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Import complete. {created} records created with status={import_status}.\n'))
