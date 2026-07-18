"""
Migration 0023 — Phase 1 Batch 4 (OLW-000017 through OLW-000021)

Moroda Bekere, Bakare Godana (provisional), Jote Tulu,
Ras Gobana Dacche, Ras Mikael of Wollo.

Note on OLW-000021:
    Fitawrari Habte Giyorgis Dinagde was considered for this slot but
    his Oromo ethnicity is disputed in the academic literature, with
    several sources describing him as Gurage rather than Oromo. Under
    the archive's two-source standard for ethnic identification, his
    inclusion cannot be justified at this time. He is replaced by
    Ras Mikael of Wollo (Muhammad Ali), whose Wollo Oromo origin is
    explicitly documented in Bahru Zewde (1991) and Harold Marcus (1975).

Note on OLW-000018:
    Bakare Godana is entered as a preliminary/unverified record based on
    regional oral tradition. The archive does not yet hold two independent
    academic sources confirming his identity, dates, or role. This record
    is flagged for replacement or upgrade when a Guji specialist or
    academic source confirms the details.
"""
from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone


NEW_RECORDS = [
    {
        'archive_id': 'OLW-000017',
        'full_name': 'Moroda Bekere',
        'alt': 'Morodaa Bekerree',
        'gender': 'M',
        'occupation': 'Mootii of Leqa Naqamte',
        'zone': 'east-wollega',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Moroda Bekere was the Mootii, or king, of the Leqa Naqamte Oromo state in present-day East Wollega "
            "and a significant figure in the political history of western Oromia during the nineteenth century. "
            "He is identified in scholarship on the Leqa Naqamte state as the predecessor and father of "
            "Kumsa Moroda (OLW-000004), who became the final Mootii before the kingdom's submission to the "
            "expanding Ethiopian Empire in 1892. Under Moroda Bekere's leadership, Leqa Naqamte maintained "
            "political authority over the surrounding Wollega region during a period of increasing external "
            "pressure from neighbouring states and later from Menelik II's expanding empire. The palace in "
            "Naqamte that later became associated with his son is part of the physical heritage of the "
            "Leqa Naqamte royal line that Moroda Bekere headed. Scholarship on the Leqa states by Tesema "
            "Ta'a documents the political structure of the kingdom through this dynastic period."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'academic',
                'title': "Tesema Ta'a — research on the Leqa Naqamte state and western Oromia political history",
                'url': '',
                'excerpt': "Tesema Ta'a's scholarship on the Wollega Oromo kingdoms documents the Leqa Naqamte "
                           "political structure and its rulers in the nineteenth century.",
            },
            {
                'source_type': 'other',
                'title': 'Oromia Culture and Tourism Bureau — Kumsa Moroda Palace',
                'url': 'https://www.oromiatourism.gov.et/index.php/tour/historical-attractions/historical-heritages/kumsa-moroda-palace',
                'excerpt': 'Documents the Leqa Naqamte royal heritage at the Naqamte palace site.',
            },
        ],
        'verification_status': 'partial',
        'notes': (
            "The dynastic relationship between Moroda Bekere and Kumsa Moroda requires confirmation from "
            "primary scholarly sources such as Tesema Ta'a\u2019s published work on Leqa Naqamte. "
            "Confirm preferred Afaan Oromo spelling of his name."
        ),
    },
    {
        'archive_id': 'OLW-000018',
        'full_name': 'Bakare Godana',
        'alt': 'Bakaree Godaanaa',
        'gender': 'M',
        'occupation': 'Guji Oromo leader (traditional account)',
        'zone': 'guji',
        'category': 'political',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Bakare Godana is preserved in Guji Oromo oral tradition as a significant leader of the Guji "
            "during the pre-1960 Foundation period. The Guji Oromo maintained an independent political "
            "and social structure under the Gadaa system through the late nineteenth and early twentieth "
            "centuries. Their encounters with Menelik II\u2019s expanding empire in the 1880s and 1890s "
            "are documented in the broader historical literature on southern Oromia, though specific "
            "named Guji leaders of this era receive limited coverage in the currently available academic "
            "record. This profile is a preliminary entry based on regional oral tradition. "
            "It requires independent academic verification\u2014ideally from a specialist in Guji history "
            "or from primary archival sources\u2014before it can be considered an established record. "
            "Researchers and community contributors with access to Guji historical sources are encouraged "
            "to contact the archive."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'other',
                'title': 'Guji oral historical tradition \u2014 preliminary record pending academic verification',
                'url': '',
                'excerpt': (
                    "This record is based on oral tradition and has not yet been confirmed by two "
                    "independent academic sources. It is flagged for upgrade or replacement."
                ),
            },
        ],
        'verification_status': 'unverified',
        'notes': (
            "PRELIMINARY RECORD. Not yet supported by two independent academic sources. "
            "Oral tradition only at this stage. Must be verified by a Guji historian or specialist "
            "before this profile advances beyond unverified status. Candidate for replacement if "
            "a better-documented Guji figure is identified."
        ),
    },
    {
        'archive_id': 'OLW-000019',
        'full_name': 'Jote Tulu',
        'alt': 'Joote Tulluu; Jote Tulu Waqayo',
        'gender': 'M',
        'occupation': 'Mootii of Leqa Qellem',
        'zone': 'kelem-wollega',
        'category': 'political',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Jote Tulu, also known as Jote Tulu Waqayo, was the Mootii of Leqa Qellem in western Oromia, "
            "the area now known as Kelem Wollega. He was one of the most significant Oromo rulers in the "
            "Wollega region during the late nineteenth century and one of the last to maintain meaningful "
            "resistance against the expansion of Menelik II\u2019s Ethiopian empire into western Oromia. "
            "Historical scholarship on the Menelik period documents the campaigns led by Ras Gobana Dacche "
            "(OLW-000020) that brought increasing pressure on western Oromo kingdoms from the 1880s onwards. "
            "Jote Tulu eventually submitted to Menelik\u2019s forces, marking the end of Leqa Qellem\u2019s "
            "independent political existence. Like other western Oromo rulers of the period, his story "
            "reflects the political complexity facing Oromo states confronted with the choice between "
            "resistance and negotiated submission. Scholarship by R.H.K. Darkwah and Tesema Ta\u2019a "
            "documents the campaigns that drew Leqa Qellem into the Ethiopian imperial system."
        ),
        'circumstances': 'Submitted to Menelik II\u2019s expanding empire following campaigns led by Ras Gobana Dacche in the 1880s\u20131890s.',
        'sources': [
            {
                'source_type': 'book',
                'title': "Darkwah, R.H.K. Shewa, Menelik and the Ethiopian Empire, 1813\u20131889 (Heinemann, 1975)",
                'url': '',
                'excerpt': 'Documents the military campaigns of Ras Gobana Dacche and the submission of western Oromo kingdoms including Leqa Qellem.',
            },
            {
                'source_type': 'academic',
                'title': "Tesema Ta'a — scholarship on the Oromo of western Wollega and the Leqa states",
                'url': '',
                'excerpt': 'Documents the political structure and leadership of the Leqa kingdoms, including Leqa Qellem, in the nineteenth century.',
            },
        ],
        'verification_status': 'partial',
        'notes': (
            "Confirm preferred Afaan Oromo spelling and personal name. Verify the precise dates of his "
            "submission and the terms under which Leqa Qellem was incorporated. Cross-reference with "
            "OLW-000020 (Ras Gobana Dacche). A third source would strengthen this profile."
        ),
    },
    {
        'archive_id': 'OLW-000020',
        'full_name': 'Ras Gobana Dacche',
        'alt': 'Gobana Daaccee; Ras Gobena Dache',
        'gender': 'M',
        'occupation': 'Military commander and political leader under Menelik II',
        'zone': 'shewa',
        'category': 'commander',
        'birth_year': 1821,
        'death_year': 1889,
        'story': (
            "Ras Gobana Dacche was an Oromo military commander of Tulama Oromo background from Shewa who "
            "became one of the most consequential and most contested figures in Oromo and Ethiopian history. "
            "Born around 1821, he rose to become the principal military commander under Menelik II, leading "
            "campaigns from the 1870s through the 1880s that substantially expanded the Ethiopian state into "
            "Oromo and other southern territories. Among the areas incorporated through his military "
            "leadership were Arsi, Guji, Bale, Leqa Qellem, parts of Hararghe, Kaffa, and others. He died "
            "in 1889 before the Battle of Adwa. "
            "\n\n"
            "Historical interpretation of Ras Gobana Dacche\u2019s role differs significantly across "
            "scholarly and popular accounts, and the archive presents these differing views without "
            "resolving the debate. "
            "\n\n"
            "Within traditional Ethiopian imperial historiography, he has been portrayed as a loyal and "
            "militarily brilliant general whose campaigns contributed to the territorial consolidation of "
            "modern Ethiopia and whose Oromo background demonstrated the possibility of advancement within "
            "the imperial system. "
            "\n\n"
            "A substantial body of Oromo scholarship and popular memory takes a sharply different view. "
            "In this perspective, Ras Gobana was an Oromo leader who facilitated the conquest and "
            "subjugation of his own people and other southern nations, enabling the loss of Oromo "
            "political independence and the imposition of the neftegna-gabbar system of extraction and "
            "land dispossession that shaped Oromo social conditions for generations. Some scholarship "
            "in this tradition treats him as the most consequential collaborator in the conquest of Oromia. "
            "\n\n"
            "A third position in the academic literature emphasises the structural constraints of his "
            "position: an Oromo military figure operating within an Amhara-dominated political hierarchy "
            "during an era of extreme regional turbulence and external (particularly European) colonial "
            "pressure on the entire Horn of Africa. Scholars who take this view argue that reducing his "
            "life to collaboration misses the complex negotiations and limited choices available to Oromo "
            "actors within the late-nineteenth-century Ethiopian state. "
            "\n\n"
            "This profile presents all three interpretations as part of the documented historical record. "
            "Researchers, family members, and community contributors are encouraged to submit additional "
            "documentation. The archive will not adjudicate between these positions."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Darkwah, R.H.K. Shewa, Menelik and the Ethiopian Empire, 1813\u20131889 (Heinemann, 1975)",
                'url': '',
                'excerpt': 'Primary scholarly account documenting Ras Gobana\u2019s military campaigns and role in the expansion of Menelik\u2019s empire.',
            },
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Cambridge University Press, 1990)",
                'url': '',
                'excerpt': 'Provides an Oromo-centred scholarly framework for understanding the conquest period and the role of intermediary figures.',
            },
            {
                'source_type': 'book',
                'title': "Bahru Zewde. A History of Modern Ethiopia, 1855\u20131991 (James Currey, 1991)",
                'url': '',
                'excerpt': 'Places Ras Gobana within the broader narrative of nineteenth-century Ethiopian state formation.',
            },
        ],
        'verification_status': 'partial',
        'notes': (
            "One of the most debated figures in Oromo historical memory. The archive intentionally preserves "
            "competing interpretations and does not endorse any single view. Birth year c. 1821 is an "
            "approximation; confirm from primary sources. Cross-reference: OLW-000019 (Jote Tulu, whose "
            "territory Gobana\u2019s campaigns incorporated), OLW-000004 (Kumsa Moroda), OLW-000003 (Abba Jifar II)."
        ),
    },
    {
        'archive_id': 'OLW-000021',
        'full_name': 'Ras Mikael of Wollo',
        'alt': 'Muhammad Ali; Negus Mikael; Ras Mika\u02bcel',
        'gender': 'M',
        'occupation': 'King of Wollo, military leader and political figure',
        'zone': 'north-shewa-oromia',
        'category': 'political',
        'birth_year': 1850,
        'death_year': 1918,
        'story': (
            "Ras Mikael of Wollo, born Muhammad Ali around 1850, was of Wollo Oromo background from "
            "north-central Ethiopia. He converted to Christianity and was baptised Mikael. He later became "
            "King of Wollo (from 1876), adopting the title Ras after aligning himself with Menelik II, and "
            "participating in the Battle of Adwa in 1896. His Wollo Oromo origin and conversion story are "
            "documented explicitly in the principal academic histories of the period. "
            "\n\n"
            "He is the father of Lij Iyasu (Emperor Iyasu V, r. 1913\u20131916), whose brief reign was "
            "marked by an attempt to reverse the political and religious marginalisation of Oromo and Muslim "
            "populations in Ethiopia\u2014a policy connected, in part, to his Wollo Oromo heritage through "
            "his father. "
            "\n\n"
            "Ras Mikael\u2019s historical significance for the Oromo Foundation record lies in two areas: "
            "first, as a documented Wollo Oromo who reached the highest levels of Ethiopian imperial power "
            "in the nineteenth century; and second, as the father whose lineage shaped Lij Iyasu\u2019s "
            "political identity and ambitions. He was defeated at the Battle of Sagl\u00e9 (October 1916) "
            "while attempting to restore his deposed son, and died in captivity in 1918. "
            "\n\n"
            "Note on zone placement: Wollo is not within the current administrative boundaries of Oromia "
            "Region. This profile is placed in North Shewa (Oromia) as the closest available zone, but "
            "researchers should note that Ras Mikael\u2019s homeland was the historically Oromo area of "
            "Wollo, which now falls within Amhara Region. A future expansion of the archive\u2019s "
            "geographic coverage to include historically Oromo areas outside current Oromia may allow "
            "more precise placement. "
            "\n\n"
            "Note on OLW-000021 candidacy: Fitawrari Habte Giyorgis Dinagde was originally proposed for "
            "this slot. His Oromo ethnicity is disputed in academic sources, with several describing him "
            "as Gurage rather than Oromo. Under the archive\u2019s two-source standard for ethnic "
            "identification, his inclusion was not justified at this time."
        ),
        'circumstances': 'Defeated at the Battle of Sagl\u00e9 (October 1916) while attempting to restore Lij Iyasu; died in captivity in 1918.',
        'sources': [
            {
                'source_type': 'book',
                'title': "Bahru Zewde. A History of Modern Ethiopia, 1855\u20131991 (James Currey, 1991)",
                'url': '',
                'excerpt': 'Documents Ras Mikael\u2019s Wollo Oromo background, his role in Ethiopian imperial politics, and the events surrounding Lij Iyasu\u2019s deposition.',
            },
            {
                'source_type': 'book',
                'title': "Marcus, Harold G. The Life and Times of Menelik II: Ethiopia 1844\u20131913 (Clarendon Press, 1975)",
                'url': '',
                'excerpt': 'Provides detailed documentation of Ras Mikael\u2019s political career, alliance with Menelik II, and participation in the Battle of Adwa.',
            },
        ],
        'verification_status': 'partial',
        'notes': (
            "Birth year c. 1850 is approximate; confirm from primary sources. Zone placed as North Shewa "
            "(Oromia) as closest available; actual homeland is historically Oromo Wollo, now Amhara Region. "
            "Cross-reference: Lij Iyasu (candidate for a later phase profile). Add a third source to "
            "strengthen this record."
        ),
    },
]

# PersonConnections to wire
CONNECTIONS = [
    ('Moroda Bekere', 'Kumsa Moroda', 'family', 'Father and predecessor as Mootii of Leqa Naqamte'),
    ('Kumsa Moroda', 'Moroda Bekere', 'family', 'Son and successor as Mootii of Leqa Naqamte'),
    ('Jote Tulu', 'Ras Gobana Dacche', 'opponent', 'Ras Gobana led campaigns that incorporated Jote Tulu\u2019s Leqa Qellem into the Ethiopian empire'),
    ('Ras Gobana Dacche', 'Jote Tulu', 'opponent', 'Led campaigns against Leqa Qellem; Jote Tulu eventually submitted'),
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

    # ── Bump HRW records at pks 17-21 to free OLW-000017..021 ──────────────
    for legacy in Legacy.objects.filter(pk__range=(17, 21)).order_by('pk'):
        new_id = f"OLW-{350 + legacy.pk:06d}"
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=new_id)
        print(f"  Bumped pk={legacy.pk} {legacy.full_name!r} → {new_id}")

    # ── Import new records ───────────────────────────────────────────────────
    existing = set(Legacy.objects.values_list('full_name', flat=True))
    for r in NEW_RECORDS:
        if r['full_name'] in existing:
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
        print(f"  Imported: {r['full_name']} ({r['archive_id']}) [{r['verification_status']}]")

    # ── Wire PersonConnections ───────────────────────────────────────────────
    name_map = {l.full_name: l for l in Legacy.objects.filter(
        full_name__in=[c[0] for c in CONNECTIONS] + [c[1] for c in CONNECTIONS]
    )}
    conn_count = 0
    for from_name, to_name, rel_type, desc in CONNECTIONS:
        from_l = name_map.get(from_name)
        to_l = name_map.get(to_name)
        if not from_l or not to_l:
            print(f"  ⚠ Connection skipped (missing): {from_name} → {to_name}")
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
    print(f"\nPhase 1 total: {foundation} | New connections: {conn_count} | Archive total: {total}")


def revert(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    names = [r['full_name'] for r in NEW_RECORDS]
    Legacy.objects.filter(full_name__in=names).delete()
    for legacy in Legacy.objects.filter(pk__range=(17, 21)).order_by('pk'):
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=f"OLW-{legacy.pk:06d}")


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0022_master_archive_phase1'),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
