from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone


RECORDS = [
    {
        'full_name': 'General Tadesse Birru',
        'alt': '',
        'occupation': 'Military officer and leading Macha\u2013Tulama organizer',
        'zone': 'shewa',
        'category': 'political',
        'death_year': 1975,
        'circumstances': 'Imprisoned; later killed by the Derg government in 1975. Cross-reference Phase 5 (Derg Period).',
        'story': (
            "General Tadesse Birru became one of the most prominent leaders of the Macha\u2013Tulama "
            "Self-Help Association and used public meetings to advocate dignity, education, development, "
            "and justice for Oromo communities. Following the government\u2019s suppression of the "
            "association, he was arrested and condemned to death; the sentence was later commuted to life "
            "imprisonment. He was released in 1974 and was killed by the Derg government in 1975. "
            "Because his death falls in the Derg period, his profile should also be cross-referenced in Phase 5."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response quoting pp. 156\u2013157',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Core documented record \u2014 add second biographical source. Cross-reference Phase 5.',
    },
    {
        'full_name': 'Captain Mamo Mezemir',
        'alt': '',
        'occupation': 'Macha\u2013Tulama leader, organizer, writer and activist',
        'zone': 'shewa',
        'category': 'political',
        'death_year': 1969,
        'circumstances': 'Executed in 1969 after the suppression of the Macha\u2013Tulama Self-Help Association.',
        'story': (
            "Captain Mamo Mezemir was a leading figure and secretary of the Macha\u2013Tulama Self-Help "
            "Association. Historical accounts connect him with the association\u2019s political awakening work "
            "and contacts with the Bale resistance. After the association was suppressed, he was sentenced to "
            "death and executed in 1969. His name is one of the clearest martyr records of the Macha\u2013Tulama phase."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Core documented record \u2014 verify exact execution date from an additional source.',
    },
    {
        'full_name': 'Haile Mariam Gamada',
        'alt': '',
        'occupation': 'Prominent Macha\u2013Tulama leader and Oromo nationalist',
        'zone': 'shewa',
        'category': 'political',
        'death_year': None,
        'circumstances': 'Imprisoned during the government crackdown on the Macha\u2013Tulama Self-Help Association; duration reported as three to ten years.',
        'story': (
            "Haile Mariam Gamada was identified in historical accounts as a prominent Oromo nationalist "
            "connected with the Macha\u2013Tulama Self-Help Association. Following the government\u2019s crackdown, "
            "he was among the leaders imprisoned for a period reported as between three and ten years. "
            "Further research is needed to document his birthplace, precise role, prison history and later life."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Documented in one secondary source \u2014 needs expansion.',
    },
    {
        'full_name': 'Alemu Qixxeesa',
        'alt': 'Alemu Kitessa',
        'occupation': 'Retired colonel, organizer and founding figure',
        'zone': 'shewa',
        'category': 'political',
        'death_year': None,
        'circumstances': 'Imprisoned during the crackdown on the Macha\u2013Tulama Self-Help Association; duration reported as three to ten years.',
        'story': (
            "Alemu Qixxeesa, also rendered Alemu Kitessa, is described as a retired colonel and one of the "
            "figures whose local self-help work contributed to the formation of the Macha\u2013Tulama Self-Help "
            "Association. After the association was targeted, he was among the prominent Oromo nationalists "
            "reported to have been imprisoned for between three and ten years."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Documented in one secondary source \u2014 reconcile name spelling.',
    },
    {
        'full_name': 'Makonnen Wasanu',
        'alt': '',
        'occupation': 'Macha\u2013Tulama member and Oromo nationalist',
        'zone': 'shewa',
        'category': 'political',
        'death_year': None,
        'circumstances': 'Imprisoned during the crackdown on the Macha\u2013Tulama Self-Help Association; sentence reported as three to ten years.',
        'story': (
            "Makonnen Wasanu is listed among prominent Oromo nationalists imprisoned during the suppression "
            "of the Macha\u2013Tulama Self-Help Association. The available source reports imprisonment lasting "
            "between three and ten years but does not provide a precise sentence, location or later biography. "
            "This record should remain under research until additional documentation is located."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Documented in one secondary source \u2014 needs expansion.',
    },
    {
        'full_name': 'Lamessa Boru',
        'alt': '',
        'occupation': 'Macha\u2013Tulama member and Oromo nationalist',
        'zone': 'shewa',
        'category': 'political',
        'death_year': None,
        'circumstances': 'Imprisoned during the crackdown on the Macha\u2013Tulama Self-Help Association; sentence reported as three to ten years.',
        'story': (
            "Lamessa Boru is named in historical accounts among prominent Oromo nationalists imprisoned "
            "during the government crackdown on the Macha\u2013Tulama Self-Help Association. The source places "
            "his imprisonment within a reported range of three to ten years. More evidence is needed about "
            "his organizational responsibilities, prison location and life after release."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Documented in one secondary source \u2014 needs expansion.',
    },
    {
        'full_name': 'Seifu Tasama',
        'alt': '',
        'occupation': 'Macha\u2013Tulama member and Oromo nationalist',
        'zone': 'shewa',
        'category': 'political',
        'death_year': None,
        'circumstances': 'Imprisoned during the crackdown on the Macha\u2013Tulama Self-Help Association; sentence reported as three to ten years.',
        'story': (
            "Seifu Tasama is identified among prominent Oromo nationalists imprisoned after the suppression "
            "of the Macha\u2013Tulama Self-Help Association. The cited historical account reports that members "
            "in this group received prison terms ranging from three to ten years. His name spelling, personal "
            "history and precise sentence require confirmation from additional records."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Documented in one secondary source \u2014 verify spelling.',
    },
    {
        'full_name': 'Dadi Fayisa',
        'alt': '',
        'occupation': 'Macha\u2013Tulama member and Oromo nationalist',
        'zone': 'shewa',
        'category': 'political',
        'death_year': None,
        'circumstances': 'Imprisoned during the crackdown on the Macha\u2013Tulama Self-Help Association; sentence reported as three to ten years.',
        'story': (
            "Dadi Fayisa is listed among prominent Oromo nationalists imprisoned during the crackdown on "
            "the Macha\u2013Tulama Self-Help Association. The source reports prison terms ranging from three to "
            "ten years for the named group. Additional research is needed to establish his exact role, sentence, "
            "place of imprisonment and later life."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia; ECOI research response',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Documented in one secondary source \u2014 needs expansion.',
    },
    {
        'full_name': 'Haji Adam Sado',
        'alt': '',
        'occupation': 'Supporter and alleged liaison with the Bale Oromo movement',
        'zone': 'bale',
        'category': 'political',
        'death_year': None,
        'circumstances': 'Imprisoned for alleged support of the Macha\u2013Tulama Self-Help Association and for helping establish links with the Bale Oromo movement.',
        'story': (
            "Haji Adam Sado of Bale is cited as one of the Oromo individuals accused and imprisoned for "
            "supporting the Macha\u2013Tulama Self-Help Association and helping establish connections between "
            "the association and the Bale Oromo farmer movement. His record links Phase 2 (Bale Resistance) "
            "and Phase 3 (Macha\u2013Tulama) and should be cross-referenced in both collections."
        ),
        'source_title': 'Asafa Jalata, Oromia and Ethiopia, discussion of Macha\u2013Tulama and Bale links',
        'source_url': 'https://www.ecoi.net/en/file/local/1143951/1788_1291644450_eth35418.pdf',
        'notes': 'Documented in one secondary source \u2014 needs a Bale-specific source. Cross-reference Phase 2.',
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


def import_macha_tulama(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    Zone = apps.get_model('legacies', 'Zone')
    HistoricalPeriod = apps.get_model('legacies', 'HistoricalPeriod')
    HistoricalEvent = apps.get_model('legacies', 'HistoricalEvent')
    Source = apps.get_model('legacies', 'Source')

    zones = {z.slug: z for z in Zone.objects.all()}
    period = HistoricalPeriod.objects.filter(slug='macha-tulama').first()
    event = HistoricalEvent.objects.filter(slug='macha-tulama-crackdown').first()
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
            category=r.get('category', 'political'),
            historical_period=period,
            historical_event=event,
            death_year=r.get('death_year'),
            circumstances=r.get('circumstances', ''),
            verification_status='partial',
            notes=r.get('notes', ''),
            status='APPROVED',
            approved_at=now,
        )
        legacy.save()
        Source.objects.create(
            legacy=legacy,
            source_type='academic',
            title=r['source_title'],
            url=r['source_url'],
            publication_date=None,
            excerpt=r.get('circumstances', ''),
        )
        existing.add(r['full_name'])
        created += 1

    print(f"Macha\u2013Tulama migration: {created} records created.")


def remove_macha_tulama(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    names = [r['full_name'] for r in RECORDS]
    Legacy.objects.filter(full_name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0016_import_hrw_314'),
    ]

    operations = [
        migrations.RunPython(import_macha_tulama, remove_macha_tulama),
    ]
