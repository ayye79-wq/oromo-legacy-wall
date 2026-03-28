from django.db import migrations

PHOTO_FIXES = {
    'tolosa-qottu':     'legacy_photos/tolosa_qottu.jpg',
    'asnake-lemma':     'legacy_photos/asnake_lemma.jpg',
    'fatuma-bedane':    'legacy_photos/fatuma_bedane.jpg',
    'wako-guutuu':      'legacy_photos/wako_guutuu.jpg',
    'dedo-roba':        'legacy_photos/dedo_roba.jpg',
    'sinbirroo-halake': 'legacy_photos/sinbirroo_halake.jpg',
    'dajane-gurmessa':  'legacy_photos/dajane_gurmessa.jpg',
}


def fix_photo_paths(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    for slug, correct_path in PHOTO_FIXES.items():
        updated = Legacy.objects.filter(slug=slug).update(photo=correct_path)
        if updated:
            print(f"Fixed photo path for: {slug}")


def reverse_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0008_seed_zones'),
    ]

    operations = [
        migrations.RunPython(fix_photo_paths, reverse_fix),
    ]
