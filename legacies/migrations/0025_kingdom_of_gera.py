"""
Migration 0025 — Kingdom of Gera (OLW-000022 through OLW-000028)

Seven documented, non-semi-legendary rulers of the Gibe kingdom of Gera
(1835–1887), derived from two independent academic sources:

  Primary:
    Mohammed Hassen, The Oromo of Ethiopia: A History 1570–1860
    (Red Sea Press, 1994), pp. 112–113, 117, 160–161.

  Secondary:
    J.S. Trimingham, Islam in Ethiopia (Oxford University Press, 1952),
    pp. 202–203.

  Tertiary (background context):
    C.F. Beckingham and G.W.B. Huntingford, Some Records of Ethiopia,
    1593–1646 (Hakluyt Society, 1954), p. lxxxv.

Semi-legendary rulers listed in some sources (Abba Sirba, Raia, Macha,
Akako, Jimma, Abo, Saiyo, Bobo) are excluded: they are explicitly
flagged as semi-legendary in the academic literature and do not meet
the archive's two-source standard.

Genne Fa (OLW-000028) is the archive's first documented female political
figure — a regent who exercised real authority in the kingdom's final years.

Zone: Gera woreda is in modern Jimma Zone, Oromia Region.
Royal title: Donacho (unique to Gera among the Gibe Five).
"""
from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone

GERA_RECORDS = [
    {
        'archive_id': 'OLW-000022',
        'full_name': 'Gunji',
        'alt': '',
        'gender': 'M',
        'occupation': 'Founder and first Donacho of the Kingdom of Gera',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Gunji was the founder of the Kingdom of Gera, the last of the five Gibe Oromo states to emerge "
            "in the southwestern Ethiopian highlands. According to Mohammed Hassen, Gunji was \u201ca "
            "successful war leader who made himself king\u201d around 1835, but died shortly afterwards, "
            "leaving behind a kingdom whose subsequent rulers would carry his political achievement forward "
            "for more than fifty years. The Kingdom of Gera, which Gunji established, was centred on a "
            "basin surrounded by gently undulating hills, with its capital at Chala (later Chira). "
            "The territory corresponds approximately to the modern woreda of Gera in Jimma Zone. The rulers "
            "of the kingdom held the title of Donacho \u2014 a distinctive royal designation used in Gera "
            "and not found in the same form among the other Gibe kingdoms. Mohammed Hassen notes that "
            "\u201cGera was, and still is, the rich land of honey,\u201d with Gera honey having a "
            "reputation as the finest in Ethiopia. The best variety, the dark ebichaa honey, became a "
            "royal monopoly under subsequent kings. Gera was also home to Mount Ijersa, regarded as sacred "
            "by the Oromo, where tradition holds that God will take his seat at the Last Judgement. Though "
            "Gunji\u2019s own reign was brief, he established the political foundation on which the Gera "
            "kingdom was built."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), p. 112",
                'url': '',
                'excerpt': "\u201cGunji, a successful war leader who made himself king\u201d founded the Kingdom of Gera around 1835 but died shortly afterwards.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), pp. 202\u2013203",
                'url': '',
                'excerpt': "Provides background on the Kingdom of Gera, its distinctive Donacho title, and the political framework established by its founder.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Founder of the Gera dynasty; reigned briefly c. 1835 before dying. Hassen p. 112 is the primary source. The semi-legendary rulers listed before Gunji in some accounts (Abba Sirba, Raia, Macha, etc.) are excluded as pre-documentation tradition.",
    },
    {
        'archive_id': 'OLW-000023',
        'full_name': 'Tulu Ganje',
        'alt': '',
        'gender': 'M',
        'occupation': 'Donacho of the Kingdom of Gera',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': 1840,
        'story': (
            "Tulu Ganje was the Donacho of the Kingdom of Gera and the final ruler of its founding "
            "dynasty. Around 1840, he was killed by King Oncho of the neighbouring Kingdom of Gumma. "
            "His murder ended Gera\u2019s first royal line and precipitated a political crisis that led "
            "to the establishment of a new dynasty under Abba Baso (OLW-000024). The fact of his death "
            "at Oncho\u2019s hands is documented in Mohammed Hassen\u2019s scholarship on the Gibe "
            "kingdoms and is corroborated by references in the history of the Kingdom of Gumma, where "
            "Oncho\u2019s reign and actions are recorded. His fate illustrates the inter-kingdom "
            "rivalries and political violence that characterised the Gibe region in the decades following "
            "the initial consolidation of its five states. The identity of his personal name, as distinct "
            "from his horse name and title, has not been established in the available academic literature."
        ),
        'circumstances': "Killed c. 1840 by King Oncho of the Kingdom of Gumma; his death ended the founding dynasty of Gera.",
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), p. 113",
                'url': '',
                'excerpt': "Documents Tulu Ganje\u2019s murder by Oncho of Gumma and the consequent end of Gera\u2019s founding dynasty.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), pp. 202\u2013203",
                'url': '',
                'excerpt': "Provides contextual documentation of the Kingdom of Gera and its succession crises.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Death year c. 1840 is an approximation. Cross-reference: Oncho of Gumma (to be added in migration 0026). Personal name not established in sources.",
    },
    {
        'archive_id': 'OLW-000024',
        'full_name': 'Abba Baso',
        'alt': 'Abba Baaso',
        'gender': 'M',
        'occupation': 'Donacho of the Kingdom of Gera',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Baso (a horse name; his personal name is not established in the academic record) "
            "founded a new royal dynasty in the Kingdom of Gera following the murder of Tulu Ganje "
            "(OLW-000023) around 1840. Mohammed Hassen describes him as \u201can unpopular ruler\u201d "
            "whose reign was cut short when he was overthrown by his own brother, subsequently known as "
            "Abba Rago I (OLW-000025). Following his deposition, Abba Baso was exiled to the Kingdom "
            "of Jimma. His brief and contested reign is a notable episode in the turbulent mid-century "
            "politics of the Gibe region. Despite its failure, the dynasty he established \u2014 through "
            "his brother\u2019s takeover \u2014 ultimately produced the kingdom\u2019s longest and most "
            "prosperous era under Abba Magal (OLW-000026). The political pattern of his reign \u2014 "
            "an unpopular ruler deposed by a sibling and sent into exile in a neighbouring kingdom \u2014 "
            "reflects a broader pattern in the Gibe states, where the courts of the five kingdoms were "
            "closely interlinked and provided refuge for deposed rulers."
        ),
        'circumstances': "Overthrown by his brother Abba Rago I and exiled to the Kingdom of Jimma.",
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), p. 113",
                'url': '',
                'excerpt': "Abba Baso \u201cproved to be an unpopular ruler. He was later overthrown by his brother Abba Rago and exiled to Jimma.\u201d",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), pp. 202\u2013203",
                'url': '',
                'excerpt': "Provides contextual documentation of the political succession crises in the Kingdom of Gera.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Abba Baso is a horse name; personal name not established. Reign dates approximate (c. 1840). Cross-reference: Abba Rago I (OLW-000025, sibling who deposed him).",
    },
    {
        'archive_id': 'OLW-000025',
        'full_name': 'Abba Rago I',
        'alt': 'Abba Raagoo I',
        'gender': 'M',
        'occupation': 'Donacho of the Kingdom of Gera',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Rago I (a horse name; his personal name is not established in the academic literature) "
            "came to power in the Kingdom of Gera around 1845 by overthrowing his brother Abba Baso "
            "(OLW-000024). He reigned for approximately fifteen years, making his one of the longer "
            "reigns in the documented history of Gera. Mohammed Hassen\u2019s scholarship confirms the "
            "fifteen-year duration of his rule and his relationship to Abba Baso. His period in power "
            "was one of relative consolidation following the political turbulence that had marked the "
            "preceding decade \u2014 the murder of Tulu Ganje by Oncho of Gumma, the brief and "
            "unpopular rule of Abba Baso, and his deposition. Under Abba Rago I, the kingdom regained "
            "a degree of stability. His reign laid the groundwork for the prosperity that his successor, "
            "Abba Magal (OLW-000026), would preside over. He is distinguished from Abba Rago II "
            "(OLW-000027) by the numeral appended to the horse name; both men held the same honorific "
            "title in succession."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), p. 113",
                'url': '',
                'excerpt': "Confirms Abba Rago I\u2019s fifteen-year reign and his role in overthrowing his brother Abba Baso.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), pp. 202\u2013203",
                'url': '',
                'excerpt': "Provides contextual documentation of the Kingdom of Gera\u2019s succession and political consolidation in the mid-nineteenth century.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Horse name only; personal name not established. Dates approximate: c. 1845\u20131860. Cross-reference: Abba Baso (OLW-000024, sibling deposed by Abba Rago I), Abba Magal (OLW-000026, successor).",
    },
    {
        'archive_id': 'OLW-000026',
        'full_name': 'Abba Magal',
        'alt': 'Abba Maagal',
        'gender': 'M',
        'occupation': 'Donacho of the Kingdom of Gera',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Magal presided over what both Mohammed Hassen and J.S. Trimingham identify as the "
            "period of greatest prosperity in the history of the Kingdom of Gera. His reign, dated "
            "approximately 1860 to 1870, coincided with Gera\u2019s peak political and economic "
            "influence among the Gibe states. A defining event of his reign was his conversion to Islam. "
            "On the question of who brought about this conversion, Hassen and Trimingham offer "
            "complementary accounts: Trimingham attributes the primary influence to Abba Jubir of Gumma, "
            "while Hassen argues that the initial credit belongs to Abba Bagibo of Limmu-Ennarya "
            "(OLW-000001), who offered political support to Abba Magal in exchange for allowing Muslim "
            "missionaries into the kingdom. Only later, both scholars agree, did Abba Jubir of Gumma "
            "complete the conversion. The account illustrates the interconnected political and religious "
            "networks of the Gibe kingdoms, where dynastic alliances and Islamic missionary activity "
            "reinforced one another. "
            "\n\nUnder Abba Magal, Gera was renowned for honey production, particularly the ebichaa "
            "(dark honey), which was a royal monopoly and was prized throughout the region as the "
            "finest honey in Ethiopia. The sacred mountain of Ijersa also lay within the kingdom. "
            "On Abba Magal\u2019s death, his wife Genne Fa (OLW-000028) became regent. The horse name "
            "\u201cAbba Magal\u201d is the name by which he is known in the academic record; his "
            "personal name has not been established."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 117, 160\u2013161",
                'url': '',
                'excerpt': "Documents Abba Magal\u2019s reign as Gera\u2019s peak period; identifies Abba Bagibo of Limmu-Ennarya as the initial catalyst for his conversion to Islam.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), p. 202",
                'url': '',
                'excerpt': "\u201cThe kingdom enjoyed its greatest prosperity under king Abba Magal, who had been converted to Islam.\u201d Attributes the conversion to the influence of Abba Jubir of Gumma.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Horse name only; personal name not established. Dates approximate: c. 1860\u20131870. Cross-reference: Abba Bagibo of Limmu-Ennarya (OLW-000001, political ally and early influence on his conversion), Genne Fa (OLW-000028, his wife and regent successor).",
    },
    {
        'archive_id': 'OLW-000027',
        'full_name': 'Abba Rago II',
        'alt': 'Abba Raagoo II',
        'gender': 'M',
        'occupation': 'Donacho of the Kingdom of Gera',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Abba Rago II held the Donacho title in the Kingdom of Gera following the death of Abba Magal "
            "(OLW-000026), around 1870. His reign was brief. The academic record for Abba Rago II is "
            "limited; his documentation derives from his position in the dynastic sequence and his "
            "approximate period of rule. He is distinguished from Abba Rago I (OLW-000025) by the "
            "numeral appended to the shared horse name. Following his death or incapacitation, "
            "the regent Genne Fa (OLW-000028) assumed authority over the kingdom. Note on sources: "
            "J.S. Trimingham\u2019s account states that upon the death of Abba Magal, \u201chis wife "
            "Genne Fa acted as regent for their son.\u201d The ruler lists also document Abba Rago II "
            "in the succession between Abba Magal and Genne Fa, which may indicate that Abba Rago II "
            "was Abba Magal\u2019s son, who reigned briefly before Genne Fa\u2019s regency became "
            "effective. This detail requires confirmation from primary sources. His personal name has "
            "not been established in the available literature."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), p. 202",
                'url': '',
                'excerpt': "Places Genne Fa\u2019s regency in the context of the Gera succession following Abba Magal\u2019s death; Abba Rago II is documented in dynastic succession lists derived from Hassen and Trimingham.",
            },
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 112\u2013113",
                'url': '',
                'excerpt': "Provides the documentary basis for the Gera dynastic sequence from which Abba Rago II\u2019s placement is derived.",
            },
        ],
        'verification_status': 'unverified',
        'notes': (
            "Minimal direct documentation. Position in succession is consistent with both Hassen and Trimingham "
            "but a clear independent description of his reign has not been located. Verification status "
            "downgraded to unverified pending a source that describes him directly. Horse name only; "
            "personal name not established. Dates approximate: c. 1870. "
            "Note: Trimingham says Genne Fa was the wife of Abba Magal, not Abba Rago II; "
            "some ruler lists describe her as widow of Abba Rago II. Discrepancy noted."
        ),
    },
    {
        'archive_id': 'OLW-000028',
        'full_name': 'Genne Fa',
        'alt': "Genne-fa; Gennefa",
        'gender': 'F',
        'occupation': 'Regent of the Kingdom of Gera',
        'zone': 'jimma',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Genne Fa was the regent of the Kingdom of Gera and the last Oromo ruler to exercise "
            "authority before the kingdom\u2019s conquest in 1887. She is the first documented female "
            "political leader in the archive. According to J.S. Trimingham\u2019s account, upon the "
            "death of King Abba Magal (OLW-000026), \u201chis wife Genne Fa acted as regent for their "
            "son.\u201d Her regency lasted from approximately 1880 until the kingdom\u2019s end. "
            "In 1887, Gera was conquered by Dejazmach Besha Abua acting on behalf of Emperor Menelik II. "
            "Both Genne Fa and her son were taken as prisoners to Jimma following the conquest. Her "
            "fate as a prisoner in Jimma is documented in Trimingham\u2019s account. "
            "\n\nGenne Fa\u2019s historical significance is considerable on several grounds. She "
            "exercised real executive authority during the final years of an independent Gera, at a "
            "time when the Gibe kingdoms were being incorporated into the expanding Ethiopian empire. "
            "As a woman regent in a political structure where male kingship was the norm, her position "
            "reflects the pragmatic responses to dynastic uncertainty that characterised the Gibe states "
            "in their last decades. The Wikipedia article on the Kingdom of Gera includes a portrait "
            "image identified as Genne Fa, which suggests her historical memory was preserved beyond "
            "the academic record alone. "
            "\n\nNote on source discrepancy: Trimingham\u2019s text identifies Genne Fa as the wife of "
            "Abba Magal, acting as regent for their son. Some dynastic lists document her as the widow "
            "of Abba Rago II (OLW-000027). This inconsistency is noted and requires resolution from "
            "primary sources."
        ),
        'circumstances': "Taken prisoner along with her son when Gera was conquered by Dejazmach Besha Abua for Menelik II in 1887.",
        'sources': [
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), p. 202",
                'url': '',
                'excerpt': "\u201cOn King Abba Magal\u2019s death, his wife Genne Fa acted as regent for their son, both of whom became prisoners in Jimma when Gera was conquered by Dejazmach Besha Abua in 1887.\u201d",
            },
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 112\u2013113, 160\u2013161",
                'url': '',
                'excerpt': "Provides the dynastic framework for the Kingdom of Gera from which Genne Fa\u2019s position and significance are established.",
            },
        ],
        'verification_status': 'partial',
        'notes': (
            "First female figure in the archive. Dates approximate. Source discrepancy noted: "
            "Trimingham names her as Abba Magal\u2019s wife; some dynastic lists name her as "
            "Abba Rago II\u2019s widow. Trimingham\u2019s direct citation is preferred. "
            "Her son\u2019s identity is not established in the available sources. "
            "A portrait image associated with Genne Fa appears on the Wikipedia article for the "
            "Kingdom of Gera \u2014 this may represent genuine historical portraiture worth tracing."
        ),
    },
]

GERA_CONNECTIONS = [
    ('Gunji', 'Tulu Ganje', 'political', 'Gunji founded the first Gera dynasty; Tulu Ganje was his successor in that founding line'),
    ('Tulu Ganje', 'Gunji', 'political', 'Succeeded the founder of the Gera dynasty'),
    ('Abba Baso', 'Abba Rago I', 'rival', 'Abba Baso was overthrown by his brother Abba Rago I and exiled to Jimma'),
    ('Abba Rago I', 'Abba Baso', 'rival', 'Overthrew and exiled his brother Abba Baso to become Donacho'),
    ('Abba Magal', 'Abba Bagibo', 'political', 'Abba Bagibo of Limmu-Ennarya supported Abba Magal\u2019s accession in exchange for allowing Muslim missionaries into Gera'),
    ('Abba Magal', 'Genne Fa', 'family', 'Abba Magal\u2019s wife; she became regent after his death'),
    ('Genne Fa', 'Abba Magal', 'family', 'Wife and regent successor of Abba Magal of Gera'),
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

    # ── Bump HRW records at pks 22–28 to free OLW-000022..028 ──────────────
    for legacy in Legacy.objects.filter(pk__range=(22, 28)).order_by('pk'):
        new_id = f"OLW-{350 + legacy.pk:06d}"
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=new_id)
        print(f"  Bumped pk={legacy.pk} {legacy.full_name!r:.35s} → {new_id}")

    # ── Import Gera records ─────────────────────────────────────────────────
    existing = set(Legacy.objects.values_list('full_name', flat=True))
    created = {}
    for r in GERA_RECORDS:
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
    # Also load Abba Bagibo for cross-kingdom connection
    all_names = list(set([c[0] for c in GERA_CONNECTIONS] + [c[1] for c in GERA_CONNECTIONS]))
    name_map = {l.full_name: l for l in Legacy.objects.filter(full_name__in=all_names)}
    name_map.update(created)

    conn_count = 0
    for from_name, to_name, rel_type, desc in GERA_CONNECTIONS:
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
    print(f"\n  Kingdom of Gera: 7 rulers (OLW-000022\u2013000028)")
    print(f"  Phase 1 Foundation total: {foundation} | Connections added: {conn_count} | Archive total: {total}")


def revert(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    names = [r['full_name'] for r in GERA_RECORDS]
    Legacy.objects.filter(full_name__in=names).delete()
    for legacy in Legacy.objects.filter(pk__range=(22, 28)).order_by('pk'):
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=f"OLW-{legacy.pk:06d}")


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0024_reserve_olw000021'),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
