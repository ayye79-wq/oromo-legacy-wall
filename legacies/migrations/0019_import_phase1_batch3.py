from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone


RECORDS = [
    {
        'full_name': 'Bofo, son of Boku',
        'alt': '',
        'occupation': 'Founder of the Limmu-Ennarya royal dynasty',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Bofo, son of Boku, was a powerful Oromo war leader who emerged around the beginning of the "
            "nineteenth century and established the royal dynasty of Limmu-Ennarya. Historical accounts "
            "describe him as gaining authority through military ability and personal influence. His rise "
            "helped transform political leadership among the Limmu Oromo into a centralized monarchy. He "
            "belongs to the Foundation phase as an early state founder in the Gibe region."
        ),
        'source_type': 'other',
        'source_title': 'Kingdom of Limmu-Ennarea \u2014 historical summary drawing on Mohammed Hassen and Mordechai Abir',
        'source_url': 'https://en.wikipedia.org/wiki/Kingdom_of_Limmu-Ennarea',
        'notes': (
            "Documented founder \u2014 replace summary URL with direct academic source. "
            "The literature varies in its spelling of Boku and Bofo. Confirm royal title, death date and "
            "succession from Mohammed Hassen\u2019s history of the Oromo."
        ),
    },
    {
        'full_name': 'Abba Boke',
        'alt': '',
        'occupation': 'Founder or early unifier of the Kingdom of Gomma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Boke was an early ruler associated with the formation of the Oromo Kingdom of Gomma. "
            "Mohammed Hassen identifies him as Gomma\u2019s first king and credits him with bringing most of "
            "the kingdom, between Yacci and Dogaye, under one authority, although the Qattu area remained "
            "outside his control. His leadership laid the political foundation that his successor Abba Manno "
            "later expanded. Some traditions identify Abba Manno rather than Abba Boke as the first king; "
            "the historical record presents both accounts."
        ),
        'source_type': 'academic',
        'source_title': 'Local History of Ethiopia: Gof\u2013Gomu; based on Mohammed Hassen\u2019s study of the Oromo',
        'source_url': 'https://nai.uu.se/download/18.39fca04516faedec8b248de6/1580829011897/ORTGOF05.pdf',
        'notes': (
            "Core documented profile \u2014 dates require confirmation. "
            "Some traditions identify Abba Manno rather than Abba Boke as the first king. "
            "The final profile should present this source disagreement."
        ),
    },
    {
        'full_name': 'Abba Manno',
        'alt': '',
        'occupation': 'King of Gomma and promoter of Islam',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Manno was an early nineteenth-century king of Gomma. He completed the kingdom\u2019s "
            "territorial consolidation by annexing Qattu and supported Muslim teachers and the Qadiriya order. "
            "Historical scholarship connects his reign with the strengthening of Islam as a shared religious "
            "and political institution in Gomma. His dynasty became known as the Awuliani dynasty. Sources "
            "disagree on whether he or Abba Boke should be regarded as the first king of Gomma; this profile "
            "presents both accounts."
        ),
        'source_type': 'academic',
        'source_title': 'Local History of Ethiopia: Gof\u2013Gomu',
        'source_url': 'https://nai.uu.se/download/18.39fca04516faedec8b248de6/1580829011897/ORTGOF05.pdf',
        'notes': (
            "Core documented profile \u2014 ready for expanded sourcing. "
            "Sources disagree on whether he or Abba Boke was the first king of Gomma. "
            "Research the meaning and preferred spelling of Awuliani."
        ),
    },
    {
        'full_name': 'Abba Gomoli',
        'alt': '',
        'occupation': 'Last independent king of Limmu-Ennarya',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Gomoli was the last king of Limmu-Ennarya before the kingdom\u2019s final incorporation into "
            "Menelik II\u2019s expanding empire. He succeeded Abba Bagibo and ruled during a period of declining "
            "trade and increasing external pressure. After Limmu-Ennarya lost its independence, his son later "
            "entered the imperial political structure. Abba Gomoli belongs to the Foundation phase as the final "
            "sovereign in the Limmu-Ennarya royal line."
        ),
        'source_type': 'other',
        'source_title': 'Kingdom of Limmu-Ennarea \u2014 historical summary based on Mohammed Hassen and Beckingham & Huntingford',
        'source_url': 'https://en.wikipedia.org/wiki/Kingdom_of_Limmu-Ennarea',
        'notes': (
            "Documented ruler \u2014 exact reign dates and biography need verification. "
            "Do not confuse with Abba Gomol of Jimma. Confirm whether Gomoli, Gomol or another spelling is preferred."
        ),
    },
    {
        'full_name': 'Abba Jobir Abba Dula',
        'alt': 'Abba Jofir',
        'occupation': 'Last king of Jimma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': 1900,
        'death_year': 1988,
        'story': (
            "Abba Jobir Abba Dula, often written Abba Jofir, was a grandson of Abba Jifar II and briefly "
            "became the last king of Jimma in 1932. His short reign ended when the central government accused "
            "him of secret correspondence with Italy and imprisoned him. He later regained a political role "
            "during the Italian occupation and was imprisoned again after Italy\u2019s defeat. His life marks the "
            "final end of Jimma\u2019s monarchy and therefore belongs to the closing section of the Foundation phase. "
            "This is a legacy profile; it documents his historical position without classifying him as a martyr."
        ),
        'source_type': 'other',
        'source_title': 'Abba Jofir biography citing Paul B. Henze and Alberto Sbacchi',
        'source_url': 'https://en.wikipedia.org/wiki/Abba_Jofir',
        'notes': (
            "Documented profile \u2014 politically sensitive; requires direct-source review using Henze and Sbacchi. "
            "This is a legacy profile, not a martyr record. Biography must neutrally document allegations, "
            "Italian-era role and later imprisonment."
        ),
    },
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


def import_phase1_batch3(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    Zone = apps.get_model('legacies', 'Zone')
    HistoricalPeriod = apps.get_model('legacies', 'HistoricalPeriod')
    Source = apps.get_model('legacies', 'Source')

    zones = {z.slug: z for z in Zone.objects.all()}
    period = HistoricalPeriod.objects.filter(slug='foundation').first()
    existing = set(Legacy.objects.values_list('full_name', flat=True))
    now = timezone.now()

    created = 0
    for r in RECORDS:
        if r['full_name'] in existing:
            continue
        zone = zones.get(r['zone']) or zones.get('shewa')
        if not zone:
            continue
        slug = _unique_slug(Legacy, slugify(r['full_name'])[:200])
        legacy = Legacy(
            full_name=r['full_name'],
            alternative_spellings=r.get('alt', ''),
            slug=slug,
            occupation=r['occupation'],
            relationship_to_person='Historical record / academic source',
            zone=zone,
            story=r['story'],
            story_en=r['story'],
            original_language='en',
            category=r['category'],
            historical_period=period,
            birth_year=r.get('birth_year'),
            death_year=r.get('death_year'),
            circumstances='',
            verification_status='partial',
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
        existing.add(r['full_name'])
        created += 1

    print(f"Phase 1 Batch 3 migration: {created} records created.")


def remove_phase1_batch3(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    names = [r['full_name'] for r in RECORDS]
    Legacy.objects.filter(full_name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0018_import_phase1_foundation'),
    ]

    operations = [
        migrations.RunPython(import_phase1_batch3, remove_phase1_batch3),
    ]
