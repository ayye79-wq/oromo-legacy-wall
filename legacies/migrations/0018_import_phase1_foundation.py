from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone


RECORDS = [
    {
        'full_name': 'Abba Bagibo',
        'alt': 'Ibsa',
        'occupation': 'King of Limmu-Ennarya',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': 1861,
        'circumstances': '',
        'story': (
            "Abba Bagibo, also identified as Ibsa, ruled the Oromo kingdom of Limmu-Ennarya during the "
            "nineteenth century. Historical scholarship describes his reign as a period in which the kingdom "
            "reached major political and commercial importance. Limmu-Ennarya\u2019s capital at Saqqa became "
            "an important center on regional trade routes. He belongs to the Foundation phase as a ruler who "
            "shaped the political history of the Gibe Oromo states."
        ),
        'source_type': 'academic',
        'source_title': 'The Kingdom of Limmu Enarya: the hegemony of King Abba Bagibo',
        'source_url': 'https://www.tandfonline.com/doi/abs/10.1080/14725843.2023.2265575',
        'notes': 'Legacy figure; not classified as a martyr. Preserve Ibsa as an alternative name.',
    },
    {
        'full_name': 'Onesimos Nesib',
        'alt': 'Hiikaa, Onesimoos Nasiib, Onesimus, Onesimos, Nesib, Nasib, Nasiib',
        'occupation': 'Scholar, educator, author and Afaan Oromo translator',
        'zone': 'ilu-aba-bora',
        'category': 'intellectual',
        'birth_year': 1856,
        'death_year': 1931,
        'circumstances': '',
        'story': (
            "Born near Hurumu in present-day Ilu Abbaa Bor, Onesimos Nesib was originally named Hiikaa, "
            "meaning \u2018translator.\u2019 After being kidnapped and sold into slavery as a child, he was "
            "freed and educated through the Swedish Evangelical Mission. He became a pioneering Oromo scholar, "
            "educator and writer and led the translation of the Bible into Afaan Oromo with essential assistance "
            "from Aster Ganno. His work became an important foundation of modern written Afaan Oromo."
        ),
        'source_type': 'other',
        'source_title': 'Dictionary of African Christian Biography \u2014 Nesib, Onesimus',
        'source_url': 'https://dacb.org/stories/ethiopia/onesimus-nesib/',
        'notes': 'Core documented profile \u2014 add Oromo-language source.',
    },
    {
        'full_name': 'Abba Jifar II',
        'alt': 'Abbaa Jifaar II',
        'occupation': 'King of Jimma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': 1861,
        'death_year': 1932,
        'circumstances': '',
        'story': (
            "Abba Jifar II was the Oromo king of Jimma from the late nineteenth century until 1932. Jimma "
            "was the largest and most powerful of the Gibe Oromo monarchies, and his long reign shaped the "
            "region\u2019s government, commerce, diplomacy and Islamic institutions. His surviving palace and "
            "the historical record of the Jimma kingdom make him one of the central royal figures of the "
            "Oromo Foundation phase."
        ),
        'source_type': 'book',
        'source_title': 'Jimma Abba Jifar: An Oromo Monarchy, Ethiopia, 1830\u20131932',
        'source_url': 'https://searchworks.stanford.edu/view/4746727',
        'notes': 'Core documented profile \u2014 biography needs expansion. Legacy figure; not classified as a martyr.',
    },
    {
        'full_name': 'Kumsa Moroda',
        'alt': '',
        'occupation': 'Moti of Leqa Naqamte',
        'zone': 'east-wollega',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'circumstances': '',
        'story': (
            "Kumsa Moroda was the final Moti, or king, of the Leqa Naqamte Oromo state in Wollega. The "
            "Oromia Culture and Tourism Bureau records that he remained king of the formerly independent "
            "kingdom after its submission to the expanding Ethiopian Empire in 1892. His leadership and "
            "surviving palace in Naqamte make him an important figure in the political history of western Oromia."
        ),
        'source_type': 'other',
        'source_title': 'Oromia Culture and Tourism Bureau \u2014 Kumsa Moroda Palace',
        'source_url': 'https://www.oromiatourism.gov.et/index.php/tour/historical-attractions/historical-heritages/kumsa-moroda-palace',
        'notes': 'Core documented profile \u2014 confirm birth and death dates. Preserve title Moti/Mootii.',
    },
    {
        'full_name': 'Aster Ganno',
        'alt': '',
        'occupation': 'Writer, teacher, translator and collector of Oromo oral literature',
        'zone': 'east-wollega',
        'category': 'intellectual',
        'birth_year': 1872,
        'death_year': 1964,
        'circumstances': '',
        'story': (
            "Aster Ganno was an Oromo writer, teacher and translator whose contribution was essential to "
            "the development of written Afaan Oromo. After being freed from enslavement, she was educated at "
            "the Swedish mission school at Imkullu. She assisted Onesimos Nesib with Oromo vocabulary and idiom, "
            "helped prepare the Oromo Bible translation, compiled language materials, and recorded hundreds of "
            "Oromo riddles, stories, proverbs and songs. She later taught in Wollega. Her work preserved both "
            "language and oral culture for later generations."
        ),
        'source_type': 'academic',
        'source_title': 'Encyclopaedia Aethiopica summary and scholarly biography of Aster Ganno',
        'source_url': 'https://en.wikipedia.org/wiki/Aster_Ganno',
        'notes': 'Well documented \u2014 replace tertiary URL with direct scholarly source (Encyclopaedia Aethiopica).',
    },
    {
        'full_name': 'Sheikh Bakri Sapalo',
        'alt': 'Abubakar Garad Usman, Bakri Sapalo',
        'occupation': 'Islamic scholar, poet, teacher, historian and script inventor',
        'zone': 'east-hararghe',
        'category': 'religious',
        'birth_year': 1895,
        'death_year': 1980,
        'circumstances': '',
        'story': (
            "Sheikh Bakri Sapalo was an Oromo Muslim scholar, poet, teacher and historian from the Harar area. "
            "During the 1950s he devised a writing system for Afaan Oromo, now commonly known as the Sapalo script. "
            "He also wrote religious, historical and geographical manuscripts and taught generations of students. "
            "Although he died in 1980, the invention of his script and much of his formative work belong to the "
            "pre-1960 Foundation phase."
        ),
        'source_type': 'academic',
        'source_title': 'Hayward and Mohammed Hassan biographical research on Sheikh Bakri Sapalo',
        'source_url': 'https://en.wikipedia.org/wiki/Bakri_Sapalo',
        'notes': 'Core figure \u2014 replace tertiary URL with original Hayward & Hassan academic article.',
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


def import_phase1(apps, schema_editor):
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
        zone = zones.get(r['zone']) or zones.get('jimma') or zones.get('shewa')
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
            circumstances=r.get('circumstances', ''),
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

    print(f"Phase 1 Foundation migration: {created} records created.")


def remove_phase1(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    names = [r['full_name'] for r in RECORDS]
    Legacy.objects.filter(full_name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0017_import_macha_tulama'),
    ]

    operations = [
        migrations.RunPython(import_phase1, remove_phase1),
    ]
