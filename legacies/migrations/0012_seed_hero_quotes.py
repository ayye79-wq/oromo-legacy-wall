from django.db import migrations


HERO_QUOTES = {
    'dajane-gurmessa':  'A child who learns in their mother tongue learns to think, not just to repeat.',
    'sinbirroo-halake': 'She did not wait for the river to part — she walked through it.',
    'dedo-roba':        'The one who plants the tree never doubts the shade.',
    'wako-guutuu':      'He who preserves the seed preserves the people.',
    'fatuma-bedane':    'Every child she brought to light carried a piece of her courage.',
    'asnake-lemma':     'Memory is the only land that cannot be taken.',
    'tolosa-qottu':     'The soil remembers those who bled for it.',
}


def seed_quotes(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    for slug, quote in HERO_QUOTES.items():
        Legacy.objects.filter(slug=slug).update(quote=quote)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0011_add_quote_field'),
    ]

    operations = [
        migrations.RunPython(seed_quotes, noop),
    ]
