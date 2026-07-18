from django.db import migrations, models


def backfill_archive_ids(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    to_update = []
    for legacy in Legacy.objects.order_by('pk').iterator():
        legacy.archive_id = f"OLW-{legacy.pk:06d}"
        to_update.append(legacy)
        if len(to_update) >= 500:
            Legacy.objects.bulk_update(to_update, ['archive_id'])
            to_update = []
    if to_update:
        Legacy.objects.bulk_update(to_update, ['archive_id'])
    count = Legacy.objects.count()
    print(f"Archive IDs assigned to {count} records (OLW-{1:06d} … OLW-{Legacy.objects.order_by('-pk').first().pk:06d}).")


def clear_archive_ids(apps, schema_editor):
    Legacy = apps.get_model('legacies', 'Legacy')
    Legacy.objects.all().update(archive_id='')


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0019_import_phase1_batch3'),
    ]

    operations = [
        migrations.AddField(
            model_name='legacy',
            name='archive_id',
            field=models.CharField(
                blank=True,
                db_index=True,
                default='',
                help_text='Permanent archive identifier e.g. OLW-000001',
                max_length=12,
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='legacy',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='legacy',
            constraint=models.UniqueConstraint(
                condition=models.Q(archive_id__gt=''),
                fields=['archive_id'],
                name='legacy_archive_id_unique_nonempty',
            ),
        ),
        migrations.RunPython(backfill_archive_ids, clear_archive_ids),
    ]
