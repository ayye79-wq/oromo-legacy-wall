"""
Migration 0022 — Master Archive Phase 1 alignment

Three operations in one atomic migration:

1. RE-ASSIGN ARCHIVE IDs
   The master archive assigns OLW-000001..OLW-000016 to Phase 1 figures.
   Those IDs were previously auto-assigned to the first 16 HRW protest records
   (pks 1-16). We bump those 16 HRW records to OLW-000351..OLW-000366 and
   assign the master IDs to Phase 1.

2. IMPORT 5 NEW PHASE 1 RECORDS
   Abba Jifar I (OLW-000007), Abba Rebu (OLW-000008), Abba Bok'a (OLW-000009),
   Abba Gomol (OLW-000010), Tufa Muna (OLW-000011)

3. ENRICH EXISTING PHASE 1 RECORDS
   Update alternative_spellings, gender, occupation and notes from master.
"""
from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone


# ─── Master ID assignments ─────────────────────────────────────────────────────
# Maps full_name  →  master archive_id
MASTER_IDS = {
    'Abba Bagibo':           'OLW-000001',
    'Onesimos Nesib':        'OLW-000002',
    'Abba Jifar II':         'OLW-000003',
    'Kumsa Moroda':          'OLW-000004',
    'Aster Ganno':           'OLW-000005',
    'Sheikh Bakri Sapalo':   'OLW-000006',
    'Abba Jifar I':          'OLW-000007',
    'Abba Rebu':             'OLW-000008',
    "Abba Bok'a":            'OLW-000009',
    'Abba Gomol':            'OLW-000010',
    'Tufa Muna':             'OLW-000011',
    'Bofo, son of Boku':     'OLW-000012',
    'Abba Boke':             'OLW-000013',
    'Abba Manno':            'OLW-000014',
    'Abba Gomoli':           'OLW-000015',
    'Abba Jobir Abba Dula':  'OLW-000016',
}

# ─── Enrichment data for existing records ─────────────────────────────────────
ENRICHMENTS = {
    'Abba Bagibo': {
        'alternative_spellings': 'Ibsa; Abbaa Bagiboo',
        'notes': 'Legacy figure; not classified as a martyr. Preserve Ibsa as an alternative name.',
    },
    'Onesimos Nesib': {
        'alternative_spellings': 'Hiikaa; Onesimoos Nasiib; Onesimus Nesib',
        'gender': 'M',
        'notes': 'His birthplace is more precisely Ilu Abbaa Bor; zone may need refinement. Add Oromo-language source.',
    },
    'Abba Jifar II': {
        'alternative_spellings': 'Abbaa Jifaar II',
        'gender': 'M',
        'notes': 'Legacy figure; verify preferred Oromo spelling. Biography needs expansion.',
    },
    'Kumsa Moroda': {
        'alternative_spellings': 'Kumsa Morodaa',
        'occupation': 'Mootii of Leqa Naqamte',
        'gender': 'M',
        'notes': 'Preserve the title Mootii. Review additional scholarship on Leqa Naqamte\u2019s incorporation.',
    },
    'Aster Ganno': {
        'alternative_spellings': 'Aster Gannoo',
        'gender': 'F',
        'notes': 'She lived beyond 1960, but her defining contribution began before 1900. Replace Wikipedia URL with direct scholarly source.',
    },
    'Sheikh Bakri Sapalo': {
        'alternative_spellings': 'Abubakar Garad Usman; Bakri Sapalo',
        'gender': 'M',
        'notes': 'Cross-reference later persecution or exile only if separately documented. Replace Wikipedia URL with Hayward & Hassan article.',
    },
    'Bofo, son of Boku': {
        'alternative_spellings': 'Bofo; Boku',
        'gender': 'M',
        'notes': 'Confirm royal title, death date and succession from academic literature.',
    },
    'Abba Boke': {
        'alternative_spellings': 'Abbaa Bokkee',
        'gender': 'M',
        'notes': 'Some traditions identify Abba Manno as the first king of Gomma; preserve the disagreement.',
    },
    'Abba Manno': {
        'alternative_spellings': 'Abbaa Mannoo',
        'gender': 'M',
        'notes': "Preserve competing traditions about Gomma\u2019s first king.",
    },
    'Abba Gomoli': {
        'alternative_spellings': 'Abba Gomol; Abbaa Gomolii',
        'gender': 'M',
        'notes': 'Do not confuse with Abba Gomol of Jimma. Verify exact reign dates.',
    },
    'Abba Jobir Abba Dula': {
        'alternative_spellings': 'Abba Jofir; Abbaa Joobir Abbaa Duulaa',
        'gender': 'M',
        'notes': 'Legacy profile, not a martyr record. Use neutral language around contested allegations.',
    },
}

# ─── 5 new records ─────────────────────────────────────────────────────────────
NEW_RECORDS = [
    {
        'archive_id': 'OLW-000007',
        'full_name': 'Abba Jifar I',
        'alt': 'Sana; Abbaa Jifaar I',
        'gender': 'M',
        'occupation': 'Founder and first king of Jimma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Jifar I, also associated with the personal name Sana, was the first king of the Oromo "
            "Kingdom of Jimma. He reigned from about 1830 to 1855 and consolidated several Jimma communities "
            "into a centralized kingdom. Historical studies credit his reign with important political and "
            "administrative development and with strengthening Jimma\u2019s position in the Gibe region. He also "
            "became the first ruler of Jimma to embrace Islam, beginning a major religious transformation in "
            "the kingdom."
        ),
        'source_type': 'academic',
        'source_title': 'The Oromo Kingdom of Jimma and Political Centralization',
        'source_url': 'https://www.jstor.org/stable/41931280',
        'source_quality': 'Secondary academic',
        'verification_status': 'partial',
        'notes': 'Legacy figure; preserve Sana and Afaan Oromo spelling. Expand biography.',
    },
    {
        'archive_id': 'OLW-000008',
        'full_name': 'Abba Rebu',
        'alt': 'Abbaa Reebuu',
        'gender': 'M',
        'occupation': 'King of Jimma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Rebu succeeded Abba Jifar I as king of Jimma and ruled during the mid-nineteenth century. "
            "He inherited a kingdom that had already become a major political and commercial power in the Gibe "
            "region. His reign forms part of the royal succession that maintained Jimma\u2019s centralized political "
            "institutions before the rule of Abba Jifar II."
        ),
        'source_type': 'academic',
        'source_title': 'Local History of Ethiopia: Jima\u2013Jimonyetta',
        'source_url': 'https://nai.uu.se/download/18.39fca04516faedec8b248dfc/1580829012483/ORTJIM05.pdf',
        'source_quality': 'Historical reference compilation',
        'verification_status': 'partial',
        'notes': 'Confirm personal name, family relationships and major events of his reign.',
    },
    {
        'archive_id': 'OLW-000009',
        'full_name': "Abba Bok'a",
        'alt': 'Abba Boqa; Abba Boka',
        'gender': 'M',
        'occupation': 'King of Jimma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Bok\u2019a was a nineteenth-century king of Jimma who ruled after Abba Rebu. He belonged to "
            "the succession of Oromo monarchs who governed Jimma during the period when the kingdom developed "
            "into one of the strongest Gibe states. The currently available sources establish his place in the "
            "royal chronology, while a fuller account of his policies and life remains to be researched."
        ),
        'source_type': 'academic',
        'source_title': 'Local History of Ethiopia: Jima\u2013Jimonyetta',
        'source_url': 'https://nai.uu.se/download/18.39fca04516faedec8b248dfc/1580829012483/ORTJIM05.pdf',
        'source_quality': 'Historical reference compilation',
        'verification_status': 'partial',
        'notes': 'Preserve spelling alternatives until preferred Oromo form is confirmed.',
    },
    {
        'archive_id': 'OLW-000010',
        'full_name': 'Abba Gomol',
        'alt': 'Abbaa Gomol',
        'gender': 'M',
        'occupation': 'King of Jimma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Gomol ruled Jimma in the later nineteenth century and was the father of Abba Jifar II. His "
            "reign continued the consolidation of Jimma before the kingdom entered its longest and best-known "
            "royal period. Historical work on the Gibe states places him within the succession that linked the "
            "founding generation of Jimma\u2019s monarchy to the reign of Abba Jifar II."
        ),
        'source_type': 'academic',
        'source_title': 'The Islamization of the Gibe Region, Southwestern Ethiopia',
        'source_url': 'https://www.jstor.org/stable/41966021',
        'source_quality': 'Secondary academic',
        'verification_status': 'partial',
        'notes': 'Do not confuse with Abba Gomoli of Limmu-Ennarya. Needs fuller reign narrative.',
    },
    {
        'archive_id': 'OLW-000011',
        'full_name': 'Tufa Muna',
        'alt': 'Tuufa Munaa',
        'gender': 'M',
        'occupation': 'Gullalle Oromo leader and resistance figure',
        'zone': 'shewa',
        'category': 'fighter',
        'birth_year': None,
        'death_year': None,
        'circumstances': (
            "Defeated and killed in battle during Menelik II\u2019s conquest of the Finfinne area, according "
            "to one academic account. Circumstances of death vary across sources."
        ),
        'story': (
            "Tufa Muna is remembered as a Gullalle Oromo leader associated with the area of Finfinne before "
            "its incorporation into Menelik II\u2019s expanding kingdom. Scholarly discussions of Finfinne\u2019s "
            "history identify him as a major local leader and describe armed conflict involving his forces "
            "during the conquest of the area. One academic account states that he was defeated and killed in "
            "battle. He belongs to the Foundation phase as an early resistance leader whose life is connected "
            "to the loss of Oromo political control around Finfinne."
        ),
        'source_type': 'academic',
        'source_title': 'The Role of Oromo Cavalry Horses in the Political History of the Oromo',
        'source_url': 'https://ejol.aau.edu.et/index.php/JIKDS/article/download/4231/7897/16972',
        'source_quality': 'Secondary academic',
        'verification_status': 'unverified',
        'notes': 'Accounts of alliances and the circumstances of his death vary. Cross-check with additional scholarship.',
    },
]

# ─── PersonConnections from master ─────────────────────────────────────────────
# (from_name, to_name, relationship_type, description)
CONNECTIONS = [
    ('Onesimos Nesib', 'Aster Ganno', 'collaborator', 'Collaborated on Afaan Oromo Bible translation and language work'),
    ('Aster Ganno', 'Onesimos Nesib', 'collaborator', 'Collaborated on Afaan Oromo Bible translation and language work'),
    ('Abba Jifar I', 'Abba Rebu', 'contemporary', 'Father and successor in the Jimma royal line'),
    ('Abba Rebu', 'Abba Jifar I', 'contemporary', 'Succeeded Abba Jifar I as king of Jimma'),
    ("Abba Bok'a", 'Abba Rebu', 'contemporary', 'Succeeded Abba Rebu as king of Jimma'),
    ('Abba Gomol', "Abba Bok'a", 'contemporary', 'Succeeded Abba Bok\u2019a as king of Jimma'),
    ('Abba Jifar II', 'Abba Gomol', 'contemporary', 'Son of Abba Gomol; succeeded him as king of Jimma'),
    ('Abba Jifar II', 'Abba Jobir Abba Dula', 'contemporary', 'Grandfather of Abba Jobir Abba Dula'),
    ('Abba Jobir Abba Dula', 'Abba Jifar II', 'contemporary', 'Grandson of Abba Jifar II; last king of Jimma'),
    ('Bofo, son of Boku', 'Abba Bagibo', 'contemporary', 'Founder of the Limmu-Ennarya dynasty; ancestor of Abba Bagibo'),
    ('Abba Gomoli', 'Abba Bagibo', 'contemporary', 'Succeeded Abba Bagibo as last independent king of Limmu-Ennarya'),
    ('Abba Boke', 'Abba Manno', 'contemporary', 'Early king of Gomma; role relative to Abba Manno disputed by sources'),
    ('Abba Manno', 'Abba Boke', 'contemporary', 'King of Gomma; role relative to Abba Boke disputed by sources'),
]


def _unique_slug(Legacy, base):
    slug = base[:200]
    if not Legacy.objects.filter(slug=slug).exists():
        return slug
    for i in range(2, 9999):
        c = f"{base[:196]}-{i}"
        if not Legacy.objects.filter(slug=c).exists():
            return c
    return base[:190]


def apply(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    Zone = apps.get_model('legacies', 'Zone')
    HistoricalPeriod = apps.get_model('legacies', 'HistoricalPeriod')
    Source = apps.get_model('legacies', 'Source')
    PersonConnection = apps.get_model('legacies', 'PersonConnection')

    zones = {z.slug: z for z in Zone.objects.all()}
    period = HistoricalPeriod.objects.filter(slug='foundation').first()
    now = timezone.now()

    # ── Step 1: blank out Phase 1 archive_ids to free up the target IDs ──────
    phase1_names = list(MASTER_IDS.keys())
    Legacy.objects.filter(full_name__in=phase1_names).update(archive_id='')

    # ── Step 2: bump HRW records at pks 1-16 that currently hold OLW-000001..016 ──
    for legacy in Legacy.objects.filter(pk__lte=16).order_by('pk'):
        new_id = f"OLW-{350 + legacy.pk:06d}"
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=new_id)

    # ── Step 3: assign master IDs to existing Phase 1 records ────────────────
    for name, master_id in MASTER_IDS.items():
        updated = Legacy.objects.filter(full_name=name).update(archive_id=master_id)
        if updated:
            print(f"  ID set: {name} → {master_id}")

    # ── Step 4: enrich existing Phase 1 records ───────────────────────────────
    for name, data in ENRICHMENTS.items():
        try:
            legacy = Legacy.objects.get(full_name=name)
            for field, value in data.items():
                setattr(legacy, field, value)
            legacy.save()
        except Legacy.DoesNotExist:
            pass

    # ── Step 5: import 5 new records ─────────────────────────────────────────
    existing_names = set(Legacy.objects.values_list('full_name', flat=True))
    for r in NEW_RECORDS:
        if r['full_name'] in existing_names:
            print(f"  Skip (exists): {r['full_name']}")
            continue
        zone = zones.get(r['zone']) or zones.get('shewa')
        slug = _unique_slug(Legacy, slugify(r['full_name'])[:200])
        legacy = Legacy(
            full_name=r['full_name'],
            alternative_spellings=r.get('alt', ''),
            gender=r.get('gender', 'U'),
            slug=slug,
            archive_id=r['archive_id'],
            occupation=r['occupation'],
            relationship_to_person='Historical record / academic source',
            zone=zone,
            story=r['story'],
            story_en=r['story'],
            original_language='en',
            category=r.get('category', 'cultural'),
            historical_period=period,
            birth_year=r.get('birth_year'),
            death_year=r.get('death_year'),
            circumstances=r.get('circumstances', ''),
            verification_status=r.get('verification_status', 'partial'),
            notes=r.get('notes', ''),
            status='APPROVED',
            approved_at=now,
        )
        legacy.save()
        Source.objects.create(
            legacy=legacy,
            source_type=r['source_type'],
            title=r['source_title'],
            url=r['source_url'],
            publication_date=None,
            excerpt='',
        )
        existing_names.add(r['full_name'])
        print(f"  Imported: {r['full_name']} ({r['archive_id']})")

    # ── Step 6: wire PersonConnections ────────────────────────────────────────
    name_map = {l.full_name: l for l in Legacy.objects.filter(full_name__in=[c[0] for c in CONNECTIONS] + [c[1] for c in CONNECTIONS])}
    conn_count = 0
    for from_name, to_name, rel_type, desc in CONNECTIONS:
        from_l = name_map.get(from_name)
        to_l = name_map.get(to_name)
        if not from_l or not to_l:
            continue
        PersonConnection.objects.get_or_create(
            from_legacy=from_l,
            to_legacy=to_l,
            relationship_type=rel_type,
            defaults={'description': desc},
        )
        conn_count += 1

    total = Legacy.objects.filter(status='APPROVED').count()
    phase1_count = Legacy.objects.filter(historical_period__slug='foundation').count()
    print(f"\nPhase 1 total: {phase1_count} | Connections wired: {conn_count} | Archive total: {total}")


def revert(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    PersonConnection = apps.get_model('legacies', 'PersonConnection')
    new_names = [r['full_name'] for r in NEW_RECORDS]
    Legacy.objects.filter(full_name__in=new_names).delete()
    for legacy in Legacy.objects.filter(pk__lte=16).order_by('pk'):
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=f"OLW-{legacy.pk:06d}")
    PersonConnection.objects.filter(
        from_legacy__full_name__in=[c[0] for c in CONNECTIONS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0021_connections_schema'),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
