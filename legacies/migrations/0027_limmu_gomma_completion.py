"""
Migration 0027 — Limmu-Ennarya completion + Gomma last king

Two new records:
  OLW-000037: Abba Bulgu of Limmu-Ennarya (1861–1883)
    — the missing third ruler between Abba Bagibo and Abba Gomoli II.
    Sources: Abba Bagibo Wikipedia article (via Mordechai Abir);
             Werner J. Lange, History of the Southern Gonga (1982).

  OLW-000038: Abba Bok'a of Gomma (last king, until 1886)
    — the final Donacho of Gomma before conquest by Beshua Abue.
    Sources: Mohammed Hassen, The Oromo of Ethiopia (1994), pp. 109–110;
             Trimingham, Islam in Ethiopia (1952), p. 200.
    Disambiguated from Abba Bok'a of Jimma (OLW-000009).

One update:
  OLW-000015 (Abba Gomoli): alternative_spellings updated to include
  "Abba Gomoli II" — the form used in the official ruler list —
  to distinguish him from his grandfather Bofo's horse name Abba Gomoli I.

Gomma middle-period rulers (Abba Bagibo of Gomma, Abba Rebo of Gomma,
Abba Dula of Gomma ×2, Abba Jifar of Gomma) are deliberately excluded:
they appear in only one source (Beckingham & Huntingford ruler list) and
do not yet meet the archive's two-source standard. IDs OLW-000039 through
OLW-000043 remain reserved for these records pending a second source.
"""
from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone

NEW_RECORDS = [
    {
        'archive_id': 'OLW-000037',
        'full_name': 'Abba Bulgu of Limmu-Ennarya',
        'alt': 'Abbaa Bulguu; Abba Bulgu',
        'gender': 'M',
        'occupation': 'Supera (king) of the Kingdom of Limmu-Ennarya',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Bulgu (a horse name; his personal name is not established in the available literature) "
            "was the third Supera, or king, of the Kingdom of Limmu-Ennarya, the most influential of the "
            "Gibe Oromo states during the nineteenth century. He reigned from 1861, upon the death of his "
            "father Abba Bagibo (OLW-000001), until 1883. His succession is confirmed in the Abba Bagibo "
            "article, where he is named as Abba Bagibo\u2019s son and designated successor, and in the "
            "official ruler list of Limmu-Ennarya derived from Werner J. Lange\u2019s scholarship on "
            "the southern Gonga and Gibe kingdoms. "
            "Abba Bulgu\u2019s reign came after the kingdom\u2019s peak years under Abba Bagibo "
            "(1825\u20131861), during which Limmu-Ennarya had established itself as the wealthiest "
            "and most commercially connected of the Gibe states, serving as a key node in the "
            "long-distance coffee and slave trade. The kingdom under Abba Bulgu continued to navigate "
            "the growing external pressures from the expanding Ethiopian imperial state. His death "
            "or end of reign in 1883 was followed by the accession of Abba Gomoli II (OLW-000015), "
            "the fourth and final Supera, whose reign would end with the kingdom\u2019s annexation "
            "by Menelik II\u2019s forces in 1891. The academic documentation of Abba Bulgu\u2019s "
            "individual reign is limited to succession records; no extended narrative account of his "
            "domestic or foreign policy has been located in the available sources."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Abba Bagibo Wikipedia article (based on Mordechai Abir, Ethiopia: The Era of the Princes, Longman, 1968)",
                'url': 'https://en.wikipedia.org/wiki/Abba_Bagibo',
                'excerpt': "Lists Abba Bulgu as the son and successor of Abba Bagibo, reigning 1861\u20131883.",
            },
            {
                'source_type': 'book',
                'title': "Lange, Werner J. History of the Southern Gonga (Southwestern Ethiopia) (Franz Steiner, Wiesbaden, 1982), pp. 28\u201330",
                'url': '',
                'excerpt': "Source for the official List of Rulers of the Gibe State of Limu-\u02bcenarya; confirms Abba Bulgu\u2019s position and dates.",
            },
        ],
        'verification_status': 'partial',
        'notes': (
            "Horse name only; personal name not established. Reign 1861\u20131883 from the official ruler list. "
            "Narrative documentation of his reign is limited. Cross-reference: Abba Bagibo (OLW-000001, father "
            "and predecessor), Abba Gomoli II (OLW-000015, successor and last king)."
        ),
    },
    {
        'archive_id': 'OLW-000038',
        'full_name': 'Abba Bok\'a of Gomma',
        'alt': "Abbaa Bok'aa; Abba Boka (Gomma)",
        'gender': 'M',
        'occupation': 'Last Moti of the Kingdom of Gomma',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': 1886,
        'story': (
            "Abba Bok\u02bca (a horse name; his personal name is not established) was the last Moti of the "
            "Kingdom of Gomma, ruling until 1886 when the kingdom was conquered by Beshua Abue acting on "
            "behalf of Emperor Menelik II. The Kingdom of Gomma, with its capital at Agaro, was one of the "
            "five Gibe Oromo states and was the first of the Gibe kingdoms to fully embrace Islam, a "
            "process documented by Mohammed Hassen as central to Gomma\u2019s identity from the early "
            "nineteenth century. Under Abba Bok\u02bca\u2019s predecessors, the kingdom had promoted "
            "Qadiri Islam and developed a reputation for \u201ca high degree of civilization\u201d in "
            "farming (Hassen). Two hills within the kingdom \u2014 Sinka and Bemba \u2014 were sacred "
            "to the Oromo and served as sites of religious veneration. "
            "\n\nAbba Bok\u02bca\u2019s reign ended with the military conquest that brought Gomma into "
            "the Ethiopian imperial system. The kingdom was among the earlier of the Gibe Five to be "
            "incorporated, falling in 1886 \u2014 a year before Gera (1887), while Gumma held out until "
            "1902. The conqueror, Beshua Abue (also rendered Besha Abua in some sources), appears in "
            "both the Gera and Gomma histories as the military commander responsible for incorporating "
            "these kingdoms on behalf of Menelik II. "
            "\n\nNote on disambiguation: Abba Bok\u02bca of Gomma is a separate historical figure "
            "from Abba Bok\u02bca of Jimma (OLW-000009), who was the third king of Jimma and whose "
            "reign predated the Gomma conquest by several decades. The horse name was common across "
            "the Gibe states and should not be taken to imply any family connection."
        ),
        'circumstances': "Kingdom of Gomma conquered by Beshua Abue acting for Menelik II in 1886; fate of Abba Bok\u02bca after the conquest is not established in the available sources.",
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 109\u2013110",
                'url': '',
                'excerpt': "Documents the history of the Kingdom of Gomma, its Islamic character, and its conquest; Abba Bok\u02bca appears as the last ruler in the official dynastic sequence.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), p. 200",
                'url': '',
                'excerpt': "Confirms Gomma\u2019s annexation and the position of its last ruler in the dynastic sequence before conquest.",
            },
        ],
        'verification_status': 'partial',
        'notes': (
            "Horse name only; personal name not established. Conquest 1886 confirmed in Hassen and Trimingham. "
            "Besha Abua/Beshua Abue is the same commander who also conquered Gera in 1887. "
            "Distinct from Abba Bok\u02bca of Jimma (OLW-000009). "
            "The middle-period rulers between Abba Manno (OLW-000014) and Abba Bok\u02bca "
            "(Abba Bagibo of Gomma, Abba Rebo, Abba Dula ×2, Abba Jifar of Gomma) appear in the "
            "Beckingham & Huntingford ruler list but do not yet have a second independent source. "
            "They are excluded from the archive pending verification; IDs OLW-000039\u2013043 reserved."
        ),
    },
]

CONNECTIONS = [
    ('Abba Bulgu of Limmu-Ennarya', 'Abba Bagibo', 'family', 'Son and successor of Abba Bagibo; the third Supera of Limmu-Ennarya'),
    ('Abba Bagibo', 'Abba Bulgu of Limmu-Ennarya', 'family', 'Father and predecessor; Abba Bulgu succeeded him in 1861'),
    ('Abba Bulgu of Limmu-Ennarya', 'Abba Gomoli', 'political', 'Abba Bulgu was succeeded by Abba Gomoli II (OLW-000015), the final king of Limmu-Ennarya'),
    ('Abba Gomoli', 'Abba Bulgu of Limmu-Ennarya', 'political', 'Succeeded Abba Bulgu as the fourth and last Supera of Limmu-Ennarya'),
    ('Abba Bok\'a of Gomma', 'Abba Manno', 'political', 'Abba Bok\u02bca was the last king of Gomma, many reigns after Abba Manno (OLW-000014)'),
    ('Genne Fa', 'Abba Bok\'a of Gomma', 'political', 'Both were the final rulers of their respective Gibe kingdoms (Gera and Gomma), both conquered by Beshua Abue for Menelik II in 1887 and 1886 respectively'),
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

    # ── Bump HRW records at pks 37–38 to free OLW-000037..038 ──────────────
    for legacy in Legacy.objects.filter(pk__range=(37, 38)).order_by('pk'):
        new_id = f"OLW-{350 + legacy.pk:06d}"
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=new_id)
        print(f"  Bumped pk={legacy.pk} {legacy.full_name!r:.35s} \u2192 {new_id}")

    # ── Update OLW-000015 alt spellings to include "Abba Gomoli II" ─────────
    gomoli = Legacy.objects.filter(archive_id='OLW-000015').first()
    if gomoli:
        existing_alt = gomoli.alternative_spellings or ''
        if 'Abba Gomoli II' not in existing_alt:
            new_alt = (existing_alt + '; Abba Gomoli II').lstrip('; ')
            Legacy.objects.filter(archive_id='OLW-000015').update(alternative_spellings=new_alt)
            print(f"  Updated OLW-000015 alt spellings: added 'Abba Gomoli II'")

    # ── Import new records ───────────────────────────────────────────────────
    existing = set(Legacy.objects.values_list('full_name', flat=True))
    created = {}
    for r in NEW_RECORDS:
        if r['full_name'] in existing:
            print(f"  Skip (exists): {r['full_name']}")
            obj = Legacy.objects.get(full_name=r['full_name'])
            created[r['full_name']] = obj
            continue
        zone = zones.get(r['zone']) or zones.get('jimma')
        slug = _unique_slug(Legacy, slugify(r['full_name'])[:200])
        legacy = Legacy(
            full_name=r['full_name'],
            alternative_spellings=r.get('alt', ''),
            gender=r.get('gender', 'M'),
            slug=slug,
            archive_id=r['archive_id'],
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
            verification_status=r['verification_status'],
            notes=r['notes'],
            status='APPROVED',
            approved_at=now,
        )
        legacy.save()
        for src in r.get('sources', []):
            Source.objects.create(
                legacy=legacy,
                source_type=src['source_type'],
                title=src['title'],
                url=src.get('url', ''),
                publication_date=None,
                excerpt=src.get('excerpt', ''),
            )
        existing.add(r['full_name'])
        created[r['full_name']] = legacy
        print(f"  Imported: {r['full_name']} ({r['archive_id']}) [{r['verification_status']}]")

    # ── Wire PersonConnections ───────────────────────────────────────────────
    all_names = list(set([c[0] for c in CONNECTIONS] + [c[1] for c in CONNECTIONS]))
    name_map = {l.full_name: l for l in Legacy.objects.filter(full_name__in=all_names)}
    name_map.update(created)

    conn_count = 0
    for from_name, to_name, rel_type, desc in CONNECTIONS:
        from_l = name_map.get(from_name)
        to_l = name_map.get(to_name)
        if not from_l or not to_l:
            print(f"  \u26a0 Connection skipped (missing): {from_name} \u2192 {to_name}")
            continue
        PersonConnection.objects.get_or_create(
            from_legacy=from_l,
            to_legacy=to_l,
            relationship_type=rel_type,
            defaults={'description': desc},
        )
        conn_count += 1

    total = Legacy.objects.filter(status='APPROVED').count()
    foundation = Legacy.objects.filter(historical_period__slug='foundation').count()
    print(f"\n  Limmu-Ennarya now complete: 4 Supera rulers (OLW-000012, 000001, 000037, 000015)")
    print(f"  Gomma closing record added: OLW-000038")
    print(f"  OLW-000039..043 reserved for mid-period Gomma rulers (pending second source)")
    print(f"  Phase 1 total: {foundation} | Connections: {conn_count} | Archive total: {total}")


def revert(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    names = [r['full_name'] for r in NEW_RECORDS]
    Legacy.objects.filter(full_name__in=names).delete()
    for legacy in Legacy.objects.filter(pk__range=(37, 38)).order_by('pk'):
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=f"OLW-{legacy.pk:06d}")


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0026_kingdom_of_gumma'),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
