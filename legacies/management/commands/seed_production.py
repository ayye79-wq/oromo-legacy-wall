import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Seed production database with foundation data if empty'

    def handle(self, *args, **options):
        from legacies.models import Legacy

        fixture_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'fixtures', 'initial_data.json'
        )

        if not os.path.exists(fixture_path):
            self.stderr.write(self.style.ERROR(f'[seed] Fixture file not found: {fixture_path}'))
            raise FileNotFoundError(fixture_path)

        approved_count = Legacy.objects.filter(status='APPROVED').count()
        if approved_count >= 100:
            self.stdout.write(self.style.SUCCESS(
                f'[seed] {approved_count} approved legacies already present — skipping.'
            ))
            return

        self.stdout.write(f'[seed] Only {approved_count} approved legacies found — loading fixture...')
        call_command('loaddata', fixture_path, verbosity=1)

        self.stdout.write('[seed] Resetting PostgreSQL sequences...')
        if connection.vendor == 'postgresql':
            from django.apps import apps
            app_models = apps.get_app_config('legacies').get_models()
            reset_sql = connection.ops.sequence_reset_sql(self.style, list(app_models))
            if reset_sql:
                with connection.cursor() as cursor:
                    for sql in reset_sql:
                        cursor.execute(sql)

        count = Legacy.objects.filter(status='APPROVED').count()
        self.stdout.write(self.style.SUCCESS(f'[seed] Done — {count} approved legacies loaded.'))
