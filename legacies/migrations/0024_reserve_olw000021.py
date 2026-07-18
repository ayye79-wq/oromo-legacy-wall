"""
Migration 0024 — Reserve OLW-000021

OLW-000021 is intentionally reserved until a fully verified Foundation
figure with two independent academic sources can be identified. This
migration removes Ras Mikael of Wollo, who was prematurely assigned to
that slot in migration 0023. His profile data is preserved in 0023 and
will be re-imported under a new ID when a proper slot is assigned.

OLW-000018 (Bakare Godana) remains in the archive at unverified status
as a flagged provisional record pending Guji specialist review.
"""
from django.db import migrations


def apply(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    Source = apps.get_model('legacies', 'Source')

    legacy = Legacy.objects.filter(archive_id='OLW-000021').first()
    if legacy:
        Source.objects.filter(legacy=legacy).delete()
        print(f"  Removed: {legacy.full_name} (OLW-000021 — reserved)")
        legacy.delete()
    else:
        print("  OLW-000021 already clear.")

    total = Legacy.objects.filter(status='APPROVED').count()
    foundation = Legacy.objects.filter(historical_period__slug='foundation').count()
    print(f"  Phase 1 total: {foundation} | Archive total: {total}")
    print("  OLW-000021: RESERVED — awaiting a fully verified Foundation figure.")


def revert(apps, schema_editor):
    # Re-import is handled by re-running migration 0023 if needed.
    # This reverse is intentionally a no-op to avoid re-populating
    # a reserved slot without proper editorial review.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0023_import_phase1_batch4'),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
