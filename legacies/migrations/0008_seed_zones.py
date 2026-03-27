from django.db import migrations

ZONES = [
    (1,  'Bale',                    'bale'),
    (2,  'Arsi',                    'arsi'),
    (3,  'Borana',                  'borana'),
    (4,  'Shewa',                   'shewa'),
    (5,  'West Shewa',              'west-shewa'),
    (6,  'East Shewa',              'east-shewa'),
    (7,  'North Shewa (Oromia)',    'north-shewa-oromia'),
    (8,  'South West Shewa',        'south-west-shewa'),
    (9,  'West Arsi',               'west-arsi'),
    (10, 'Borena',                  'borena'),
    (11, 'Guji',                    'guji'),
    (12, 'East Guji',               'east-guji'),
    (13, 'West Guji',               'west-guji'),
    (14, 'East Hararghe',           'east-hararghe'),
    (15, 'West Hararghe',           'west-hararghe'),
    (16, 'Jimma',                   'jimma'),
    (17, 'Ilu Aba Bora',            'ilu-aba-bora'),
    (18, 'Buno Bedele',             'buno-bedele'),
    (19, 'Kelem Wollega',           'kelem-wollega'),
    (20, 'East Wollega',            'east-wollega'),
    (21, 'West Wollega',            'west-wollega'),
    (22, 'Horo Guduru Wollega',     'horo-guduru-wollega'),
]


def seed_zones(apps, schema_editor):
    Zone = apps.get_model('legacies', 'Zone')
    for pk, name, slug in ZONES:
        Zone.objects.get_or_create(pk=pk, defaults={'name': name, 'slug': slug})


def unseed_zones(apps, schema_editor):
    Zone = apps.get_model('legacies', 'Zone')
    Zone.objects.filter(pk__in=[z[0] for z in ZONES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0007_add_relationship_to_person'),
    ]

    operations = [
        migrations.RunPython(seed_zones, unseed_zones),
    ]
