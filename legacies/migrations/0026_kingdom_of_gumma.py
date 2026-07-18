"""
Migration 0026 — Kingdom of Gumma (OLW-000029 through OLW-000036)

Eight documented rulers of the Gibe kingdom of Gumma (c. 1770–1902),
the most populous of the Gibe Five and the last to be finally subdued.
Derived from two independent academic sources:

  Primary:
    Mohammed Hassen, The Oromo of Ethiopia: A History 1570–1860
    (Red Sea Press, 1994), pp. 115–116.

  Secondary:
    C.F. Beckingham and G.W.B. Huntingford, Some Records of Ethiopia,
    1593–1646 (Hakluyt Society, 1954), p. lxxix.

  Supplementary:
    J.S. Trimingham, Islam in Ethiopia (Oxford University Press, 1952).

Zone: Gumma's territory corresponds to the modern woredas of Gechi,
Borecha, and Didessa — all within Ilu Aba Bora Zone, Oromia Region.

Notable: Firisa (OLW-000036) declared a jihad against imperial rule in 1899
and was not captured until 1902. His resistance is among the last documented
acts of political independence by a Gibe ruler.

Note on 'Adam' (OLW-000029): Mohammed Hassen suggests the tradition around
Adam as founder was "invented so as to Islamize the original founder of the
dynasty." The profile presents this scholarly caveat honestly.
"""
from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone

GUMMA_RECORDS = [
    {
        'archive_id': 'OLW-000029',
        'full_name': 'Adam of Gumma',
        'alt': 'Adam, Founder of Gumma',
        'gender': 'M',
        'occupation': 'Founder of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Adam is recorded as the founder of the royal dynasty of the Kingdom of Gumma, the most "
            "populous of the five Gibe Oromo states, with a population estimated at around 50,000 in "
            "the 1880s. According to the tradition preserved by the reigning Gumma dynasty, Adam came "
            "to the area around 1770, helped depose the last king of the previous dynasty, and "
            "established the line that would rule Gumma until 1902. The tradition holds that he "
            "descended from a sheikh who came from Mogadishu. Mohammed Hassen, examining this "
            "tradition, suggests that the story about Adam \u201cwas invented so as to Islamize the "
            "original founder of the dynasty\u201d \u2014 that is, the tradition may reflect a later "
            "effort to give the dynasty Islamic credentials rather than an accurate genealogical memory. "
            "This scholarly caveat is presented as part of the historical record. "
            "Despite the uncertainty surrounding his origins, Adam\u2019s role as the dynastic founder "
            "is confirmed in the academic literature. The kingdom he established was described as "
            "located on a high plateau at an average elevation of 6,500 feet, and its inhabitants "
            "had a widespread reputation as warriors. Gumma would endure as an independent state for "
            "approximately 130 years before final imperial conquest in 1902."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 115\u2013116",
                'url': '',
                'excerpt': "Documents Adam as the dynastic founder of Gumma c. 1770 and critically examines the tradition, noting it may have been \u201cinvented so as to Islamize the original founder of the dynasty.\u201d",
            },
            {
                'source_type': 'book',
                'title': "Beckingham, C.F. and Huntingford, G.W.B. Some Records of Ethiopia, 1593\u20131646 (Hakluyt Society, 1954), p. lxxix",
                'url': '',
                'excerpt': "Documents the Kingdom of Gumma, its territory, and the founding tradition.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Foundation date c. 1770 is an approximation. Hassen questions whether the tradition around Adam accurately reflects the dynasty\u2019s origins or was later embellished. Include this caveat visibly.",
    },
    {
        'archive_id': 'OLW-000030',
        'full_name': 'Jilcha of Gumma',
        'alt': 'Jilchaa',
        'gender': 'M',
        'occupation': 'Moti of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Jilcha ruled the Kingdom of Gumma around 1795, succeeding the dynasty founder Adam. He "
            "is documented in the academic succession records of the Gumma dynasty derived from "
            "Mohammed Hassen\u2019s scholarship on the Gibe kingdoms. Beyond his place in the "
            "succession, the available academic literature does not provide a detailed narrative of "
            "his reign. His period falls within the early phase of the kingdom\u2019s documented "
            "history, before the better-documented reigns of Oncho and Jawe. The kingdom during "
            "this period was consolidating its territory and establishing the political structures "
            "that would characterise it through the nineteenth century."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 115\u2013116",
                'url': '',
                'excerpt': "Documents the succession of Gumma kings in the early nineteenth century.",
            },
            {
                'source_type': 'book',
                'title': "Beckingham, C.F. and Huntingford, G.W.B. Some Records of Ethiopia, 1593\u20131646 (Hakluyt Society, 1954), p. lxxix",
                'url': '',
                'excerpt': "Background documentation of the Kingdom of Gumma and its ruling dynasty.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Limited documentation beyond succession placement. Reign date c. 1795 is approximate. A third independent source describing his reign would strengthen this profile.",
    },
    {
        'archive_id': 'OLW-000031',
        'full_name': 'Oncho of Gumma',
        'alt': 'Oonchoo',
        'gender': 'M',
        'occupation': 'Moti of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'cultural',
        'birth_year': None,
        'death_year': None,
        'story': (
            "Oncho ruled the Kingdom of Gumma around 1810 and is notable as the ruler whose "
            "military actions directly brought about the end of the founding dynasty of the "
            "neighbouring Kingdom of Gera. Around 1840, Oncho killed Tulu Ganje (OLW-000023), "
            "the Donacho of Gera, an act documented independently in both the Gumma and Gera "
            "academic records. The killing of a neighbouring king by Oncho illustrates the "
            "intense inter-kingdom rivalries of the Gibe region during this period, in which "
            "political violence between the five states was not uncommon. The murder of Tulu Ganje "
            "precipitated the political crisis in Gera that led to the establishment of a new "
            "Gera dynasty under Abba Baso. Oncho\u2019s reign thus had lasting consequences "
            "beyond Gumma\u2019s borders. The available sources confirm the event but do not "
            "provide an extended narrative of his domestic reign."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 113, 115\u2013116",
                'url': '',
                'excerpt': "Documents Oncho of Gumma as the ruler who killed Tulu Ganje of Gera, ending the Gera founding dynasty.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952), pp. 202\u2013203",
                'url': '',
                'excerpt': "Corroborates the political relations between Gumma and Gera, including inter-kingdom conflict.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Cross-reference: Tulu Ganje (OLW-000023) \u2014 killed by Oncho. Reign date c. 1810 is approximate. The documentation of the killing of Tulu Ganje provides firm independent confirmation from two sources.",
    },
    {
        'archive_id': 'OLW-000032',
        'full_name': 'Jawe of Gumma',
        'alt': 'Jawee',
        'gender': 'M',
        'occupation': 'Moti of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'cultural',
        'birth_year': None,
        'death_year': 1854,
        'story': (
            "Jawe ruled the Kingdom of Gumma from approximately 1840 to 1854. His reign is historically "
            "significant as the period in which Gumma formally adopted Islam. According to Mohammed "
            "Hassen, Jawe was converted to Islam by merchants from Shewa and Begemder, and \u201cin "
            "turn he imposed his religious faith upon his subjects.\u201d The conversion of Gumma "
            "under Jawe reflects a wider pattern in the Gibe region during the early-to-mid "
            "nineteenth century, in which commercial contacts with Muslim traders from northern "
            "Ethiopia facilitated the gradual Islamisation of the Gibe states. By the time of Jawe\u2019s "
            "conversion, the Kingdom of Gomma had already adopted Islam, and Gumma\u2019s own "
            "acceptance of the faith deepened the region\u2019s connection to the broader Islamic "
            "networks of the Ethiopian highlands. Jawe\u2019s imposition of Islam on his subjects "
            "shaped the religious and cultural identity of the kingdom for its remaining decades and "
            "was central to the political resistance led by his successors against Christian imperial "
            "authority."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 115\u2013116",
                'url': '',
                'excerpt': "Jawe \u201cwas converted to Islam by merchants from Shewa and Begemder, and in turn he imposed his religious faith upon his subjects.\u201d",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952)",
                'url': '',
                'excerpt': "Documents the Islamisation of the Gibe kingdoms and the role of Gumma in that process.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Reign dates approximate: c. 1840\u20131854. The account of his conversion by northern merchants and imposition of Islam on subjects is well documented in Hassen.",
    },
    {
        'archive_id': 'OLW-000033',
        'full_name': 'Abba Dula of Gumma',
        'alt': 'Abbaa Duulaa',
        'gender': 'M',
        'occupation': 'Moti of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'cultural',
        'birth_year': None,
        'death_year': 1879,
        'story': (
            "Abba Dula ruled the Kingdom of Gumma from 1854 until June 1879. His twenty-five-year "
            "reign is among the longer reigns in Gumma\u2019s documented history and covered a period "
            "of increasing political tension across the Gibe region as the external pressures that "
            "would eventually end the kingdoms\u2019 independence began to intensify. The reign of "
            "Abba Dula saw Gumma consolidate its position as a strongly Islamic state following the "
            "conversion of his predecessor Jawe. The available academic literature confirms his "
            "dates and succession but does not provide an extended narrative of his domestic policies "
            "or foreign relations. He was succeeded by Abba Jubir (OLW-000034), whose reign would be "
            "defined by the Muslim League and the first encounters with Menelik II\u2019s expanding "
            "state. Note: \u201cAbba Dula\u201d is a title meaning \u201cFather of War\u201d in Oromo "
            "and was a common Gadaa-era designation; this profile refers specifically to the Gumma "
            "ruler of this name, not to the similarly titled ruler in the Gomma dynasty."
        ),
        'circumstances': '',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 115\u2013116",
                'url': '',
                'excerpt': "Documents Abba Dula\u2019s succession from Jawe and the Gumma dynastic sequence.",
            },
            {
                'source_type': 'book',
                'title': "Beckingham, C.F. and Huntingford, G.W.B. Some Records of Ethiopia, 1593\u20131646 (Hakluyt Society, 1954), p. lxxix",
                'url': '',
                'excerpt': "Background documentation of the Gumma kingdom and its rulers.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Reign 1854\u2013June 1879. Note the title disambiguation: \u201cAbba Dula of Gumma\u201d is distinct from the \u201cAbba Dula\u201d who appears in the Gomma dynastic list. Dates from the dynastic record; narrative documentation limited.",
    },
    {
        'archive_id': 'OLW-000034',
        'full_name': 'Abba Jubir of Gumma',
        'alt': 'Abbaa Jubiir',
        'gender': 'M',
        'occupation': 'Moti of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'political',
        'birth_year': None,
        'death_year': 1890,
        'story': (
            "Abba Jubir ruled the Kingdom of Gumma from June 1879 to approximately 1890 and is one "
            "of the most politically active and documented rulers in Gumma\u2019s history. His reign "
            "was defined by two interlocking ambitions: resisting the encroachment of Menelik II\u2019s "
            "expanding empire and asserting Gumma\u2019s leadership within the Gibe region. "
            "\n\nIn 1882, Abba Jubir brokered the formation of a political and military confederacy "
            "known as the \u201cMuslim League,\u201d persuading the rulers of Ennarea, Gomma, and "
            "Jimma to join a collective response to the threat from the Macha Oromo. The league had "
            "limited military success: the member states did not consistently support one another, "
            "and Abba Jubir\u2019s own campaigns against the Macha were inconclusive. He was forced "
            "to negotiate an armistice after his elder brother Abba Digir was captured. Despite the "
            "league\u2019s military failures, its formation reflects Abba Jubir\u2019s awareness "
            "that the political landscape of the Gibe region required a collective rather than "
            "individual response. "
            "\n\nAbba Jubir also went to war against the Kingdom of Jimma \u2014 despite Jimma\u2019s "
            "participation in the Muslim League \u2014 and sacked its capital, even as Gomma and "
            "Limmu-Ennarya intervened on Jimma\u2019s behalf. This episode illustrates the limits "
            "of political solidarity in the Gibe region: even in the face of external threat, "
            "inter-kingdom rivalry could override alliance commitments. Gumma under Abba Jubir "
            "remained a stronghold of Islam and \u201cprovided asylum to men exiled from the other "
            "Gibe kingdoms.\u201d His kingdom was conquered by Menelik II\u2019s forces around 1885, "
            "though resistance continued under subsequent rulers."
        ),
        'circumstances': 'Kingdom of Gumma conquered by forces of Menelik II around 1885; Abba Jubir\u2019s reign ended c. 1890.',
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 115\u2013116",
                'url': '',
                'excerpt': "Documents Abba Jubir\u2019s formation of the Muslim League in 1882, the league\u2019s limited success, his war against Jimma, and Gumma\u2019s role as a haven for exiles.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952)",
                'url': '',
                'excerpt': "Provides broader context for the political and religious dynamics of the Gibe kingdoms during Abba Jubir\u2019s reign.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Note disambiguation: Abba Jubir of Gumma is distinct from Abba Jubir of Jimma (the last king of Jimma, OLW-000016). Reign June 1879\u2013c. 1890. Cross-reference: Abba Gomoli of Limmu-Ennarya (OLW-000015, party to the Muslim League).",
    },
    {
        'archive_id': 'OLW-000035',
        'full_name': 'Abba Fogi of Gumma',
        'alt': 'Abbaa Fogii',
        'gender': 'M',
        'occupation': 'Last recognised Moti of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'political',
        'birth_year': None,
        'death_year': 1899,
        'story': (
            "Abba Fogi was the last recognised Moti of the Kingdom of Gumma, ruling from approximately "
            "1890 until the kingdom\u2019s formal conquest in 1899. His reign coincided with the final "
            "phase of Menelik II\u2019s incorporation of the Gibe kingdoms into the Ethiopian empire. "
            "He was conquered by Ras Tessema Nadew, acting as Menelik II\u2019s representative, "
            "completing the imperial subjugation of a kingdom that had resisted or maintained "
            "semi-autonomous status since Abba Jubir\u2019s first encounter with imperial forces. "
            "Gumma under Abba Fogi\u2019s rule had long been described as \u201ca hotbed of "
            "rebellion and Muslim fanaticism against alien colonial administration.\u201d His "
            "deposition ended over a century of continuous rule by the Gumma dynasty. His son "
            "Firisa (OLW-000036), who had fled to Sudan following the conquest, would return in "
            "1899 to lead the final armed resistance against imperial rule."
        ),
        'circumstances': "Conquered by Ras Tessema Nadew acting for Menelik II; his son Firisa fled to Sudan.",
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 115\u2013116",
                'url': '',
                'excerpt': "Documents Gumma\u2019s final resistance and the circumstances of its conquest.",
            },
            {
                'source_type': 'book',
                'title': "Beckingham, C.F. and Huntingford, G.W.B. Some Records of Ethiopia, 1593\u20131646 (Hakluyt Society, 1954), p. lxxix",
                'url': '',
                'excerpt': "Documents the Kingdom of Gumma and its fate under imperial conquest.",
            },
        ],
        'verification_status': 'partial',
        'notes': "Reign dates approximate: c. 1890\u20131899. Cross-reference: Firisa (OLW-000036, his son). Ras Tessema Nadew is mentioned in the Gumma ruler list as the imperial commander who defeated him.",
    },
    {
        'archive_id': 'OLW-000036',
        'full_name': 'Firisa of Gumma',
        'alt': 'Firisaa',
        'gender': 'M',
        'occupation': 'Resistance leader and final ruler of the Kingdom of Gumma',
        'zone': 'ilu-aba-bora',
        'category': 'fighter',
        'birth_year': None,
        'death_year': 1902,
        'story': (
            "Firisa was the son of Abba Fogi (OLW-000035), the last recognised Moti of the Kingdom of "
            "Gumma. Following the conquest of the kingdom by Ras Tessema Nadew around 1899, Firisa "
            "fled to the Sudan, where he found sanctuary. In 1899, he returned to Gumma and declared "
            "a jihad against imperial rule, launching an armed uprising against the forces of Menelik II "
            "in an attempt to restore the independence of the kingdom. His uprising reflects the "
            "tenacity of Gumma\u2019s Islamic identity and the depth of resistance to imperial "
            "incorporation in the region. "
            "\n\nFirisa was eventually captured in 1902 and executed in Jimma \u2014 the same city "
            "to which his predecessor Abba Baso of Gera had been exiled, and which served as the "
            "administrative centre of Gibe region politics for decades. His execution marked the "
            "definitive end of the Kingdom of Gumma as a political entity, more than 130 years after "
            "its foundation. His story is among the last documented acts of armed political resistance "
            "by a Gibe Oromo ruler against imperial incorporation. The Kingdom of Gumma, founded "
            "c. 1770 and dissolved in 1902, endured longer than any of the other four Gibe kingdoms."
        ),
        'circumstances': "Fled to Sudan after conquest; returned 1899 to declare jihad; captured 1902 and executed in Jimma.",
        'sources': [
            {
                'source_type': 'book',
                'title': "Hassen, Mohammed. The Oromo of Ethiopia: A History 1570\u20131860 (Red Sea Press, 1994), pp. 115\u2013116",
                'url': '',
                'excerpt': "Documents Firisa\u2019s return from Sudan, his jihad declaration, and his capture and execution.",
            },
            {
                'source_type': 'book',
                'title': "Trimingham, J.S. Islam in Ethiopia (Oxford University Press, 1952)",
                'url': '',
                'excerpt': "Documents the final phase of Gumma\u2019s resistance: Firisa \u201cwas eventually captured in 1902, then executed in Jimma soon afterwards.\u201d",
            },
        ],
        'verification_status': 'partial',
        'notes': "Cross-reference: Abba Fogi of Gumma (OLW-000035, father). Death year 1902 confirmed. The Sudan exile and subsequent return are documented in both sources. His father\u2019s identity as Abba Fogi is from the dynastic record but should be confirmed from a primary source.",
    },
]

GUMMA_CONNECTIONS = [
    ('Oncho of Gumma', 'Tulu Ganje', 'opponent', 'Oncho of Gumma killed Tulu Ganje, ending the founding dynasty of the Kingdom of Gera c. 1840'),
    ('Tulu Ganje', 'Oncho of Gumma', 'opponent', 'Murdered by Oncho of Gumma c. 1840, ending Gera\u2019s founding dynasty'),
    ('Abba Jubir of Gumma', 'Abba Gomoli', 'political', 'Both were parties to the Muslim League formed in 1882 as a confederation against the Macha Oromo'),
    ('Firisa of Gumma', 'Abba Fogi of Gumma', 'family', 'Firisa was the son of Abba Fogi, the last Moti of Gumma; he fled to Sudan after his father\u2019s conquest and returned to lead the final resistance'),
    ('Abba Fogi of Gumma', 'Firisa of Gumma', 'family', 'Father of Firisa; his defeat by Ras Tessema Nadew led Firisa to flee to Sudan before returning to lead the 1899 uprising'),
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

    # ── Bump HRW records at pks 29–36 to free OLW-000029..036 ──────────────
    for legacy in Legacy.objects.filter(pk__range=(29, 36)).order_by('pk'):
        new_id = f"OLW-{350 + legacy.pk:06d}"
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=new_id)
        print(f"  Bumped pk={legacy.pk} {legacy.full_name!r:.35s} \u2192 {new_id}")

    # ── Import Gumma records ─────────────────────────────────────────────────
    existing = set(Legacy.objects.values_list('full_name', flat=True))
    created = {}
    for r in GUMMA_RECORDS:
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
    all_names = list(set([c[0] for c in GUMMA_CONNECTIONS] + [c[1] for c in GUMMA_CONNECTIONS]))
    name_map = {l.full_name: l for l in Legacy.objects.filter(full_name__in=all_names)}
    name_map.update(created)

    conn_count = 0
    for from_name, to_name, rel_type, desc in GUMMA_CONNECTIONS:
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
    print(f"\n  Kingdom of Gumma: 8 rulers (OLW-000029\u2013000036)")
    print(f"  Phase 1 Foundation total: {foundation} | Connections: {conn_count} | Archive total: {total}")


def revert(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    names = [r['full_name'] for r in GUMMA_RECORDS]
    Legacy.objects.filter(full_name__in=names).delete()
    for legacy in Legacy.objects.filter(pk__range=(29, 36)).order_by('pk'):
        Legacy.objects.filter(pk=legacy.pk).update(archive_id=f"OLW-{legacy.pk:06d}")


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0025_kingdom_of_gera'),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
