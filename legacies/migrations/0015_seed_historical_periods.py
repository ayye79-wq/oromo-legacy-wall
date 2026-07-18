from django.db import migrations


PERIODS = [
    {
        'order': 1,
        'slug': 'foundation',
        'name': 'The Foundation Era',
        'years_label': 'Before 1960',
        'years_start': None,
        'years_end': 1959,
        'description': 'Religious leaders, kings, chiefs, resistance leaders, intellectuals, and cultural figures who shaped Oromo identity before the modern era.',
    },
    {
        'order': 2,
        'slug': 'bale-resistance',
        'name': 'Bale Resistance',
        'years_label': '1963–1970',
        'years_start': 1963,
        'years_end': 1970,
        'description': 'The armed uprising in Bale province — fighters, commanders, civilians killed, and political leaders of the Bale rebellion.',
    },
    {
        'order': 3,
        'slug': 'macha-tulama',
        'name': 'Macha Tulama Movement',
        'years_label': '1960s',
        'years_start': 1963,
        'years_end': 1969,
        'description': 'Leaders of the Macha and Tulama Self-Help Association, including those imprisoned or killed for Oromo political organization.',
    },
    {
        'order': 4,
        'slug': 'early-olf',
        'name': 'Early OLF Era',
        'years_label': '1973–1991',
        'years_start': 1973,
        'years_end': 1991,
        'description': 'Founders, political leaders, military commanders, students, writers, and journalists of the early Oromo Liberation Front period.',
    },
    {
        'order': 5,
        'slug': 'derg',
        'name': 'Derg Period',
        'years_label': '1974–1991',
        'years_start': 1974,
        'years_end': 1991,
        'description': 'One of the largest collections. Thousands of Oromo killed under the Derg military junta — by zone, year, prison, and massacre.',
    },
    {
        'order': 6,
        'slug': 'transitional',
        'name': 'Transitional Government',
        'years_label': '1991',
        'years_start': 1991,
        'years_end': 1991,
        'description': 'Political killings, disappearances, and executions during the 1991 transitional period.',
    },
    {
        'order': 7,
        'slug': 'eprdf',
        'name': 'EPRDF Era',
        'years_label': '1991–2014',
        'years_start': 1991,
        'years_end': 2014,
        'description': 'Political activists, students, journalists, community leaders, and religious leaders persecuted or killed under EPRDF rule.',
    },
    {
        'order': 8,
        'slug': 'protests-2014-2018',
        'name': 'Oromo Protests',
        'years_label': '2014–2018',
        'years_start': 2014,
        'years_end': 2018,
        'description': 'Every documented victim of the Oromo protests — sourced from HRW, Amnesty International, Qeerroo, OMN, newspapers, and family submissions.',
    },
    {
        'order': 9,
        'slug': 'irreecha-2016',
        'name': 'Irreecha 2016',
        'years_label': 'October 2, 2016',
        'years_start': 2016,
        'years_end': 2016,
        'description': 'A separate collection documenting every victim of the Irreecha massacre at Bishoftu, cross-referenced from multiple sources.',
    },
    {
        'order': 10,
        'slug': 'transition-2018',
        'name': '2018 Political Transition',
        'years_label': '2018',
        'years_start': 2018,
        'years_end': 2018,
        'description': 'The closing chapter of Volume One — events and lives documented through the 2018 political transition.',
    },
]

EVENTS = [
    {
        'slug': 'irreecha-massacre-2016',
        'name': 'Irreecha Massacre',
        'event_date': '2016-10-02',
        'period_slug': 'irreecha-2016',
        'description': 'Security forces fired on tens of thousands of Oromo gathered for the Irreecha thanksgiving festival at Bishoftu lake, killing dozens to hundreds.',
    },
    {
        'slug': 'bale-uprising',
        'name': 'Bale Uprising',
        'event_date': '1963-01-01',
        'period_slug': 'bale-resistance',
        'description': 'Armed peasant uprising in Bale province against imperial land policy and ethnic discrimination.',
    },
    {
        'slug': 'macha-tulama-crackdown',
        'name': 'Macha Tulama Crackdown',
        'event_date': '1967-01-01',
        'period_slug': 'macha-tulama',
        'description': 'Imperial government banning and mass arrest of Macha and Tulama Self-Help Association leaders.',
    },
    {
        'slug': 'addis-ababa-master-plan-protests',
        'name': 'Addis Ababa Master Plan Protests',
        'event_date': '2014-04-25',
        'period_slug': 'protests-2014-2018',
        'description': 'Mass protests against the Addis Ababa Integrated Development Master Plan that threatened Oromo farmers.',
    },
]


def seed_periods(apps, schema_editor):
    HistoricalPeriod = apps.get_model('legacies', 'HistoricalPeriod')
    HistoricalEvent = apps.get_model('legacies', 'HistoricalEvent')

    period_map = {}
    for p in PERIODS:
        obj, _ = HistoricalPeriod.objects.get_or_create(
            slug=p['slug'],
            defaults={k: v for k, v in p.items() if k != 'slug'}
        )
        period_map[p['slug']] = obj

    for e in EVENTS:
        period = period_map.get(e['period_slug'])
        HistoricalEvent.objects.get_or_create(
            slug=e['slug'],
            defaults={
                'name': e['name'],
                'event_date': e['event_date'],
                'period': period,
                'description': e['description'],
            }
        )


def unseed_periods(apps, schema_editor):
    HistoricalPeriod = apps.get_model('legacies', 'HistoricalPeriod')
    HistoricalEvent = apps.get_model('legacies', 'HistoricalEvent')
    slugs = [p['slug'] for p in PERIODS]
    event_slugs = [e['slug'] for e in EVENTS]
    HistoricalEvent.objects.filter(slug__in=event_slugs).delete()
    HistoricalPeriod.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0014_phase_a_archive_fields'),
    ]

    operations = [
        migrations.RunPython(seed_periods, unseed_periods),
    ]
