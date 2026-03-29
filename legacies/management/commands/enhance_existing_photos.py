"""
Management command: trigger AI enhancement for all heroes that have a photo
but haven't been enhanced yet.

Usage:
    python manage.py enhance_existing_photos
"""
import time
import logging
from django.core.management.base import BaseCommand
from legacies.models import Legacy
from legacies.enhance import _run_enhancement

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Trigger AI photo enhancement for all unenhanced heroes with photos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--slugs',
            nargs='+',
            help='Only enhance specific slugs',
        )

    def handle(self, *args, **options):
        qs = Legacy.objects.filter(
            photo__isnull=False,
            photo_enhancement_status__in=['none', 'failed'],
        ).exclude(photo='')

        if options.get('slugs'):
            qs = qs.filter(slug__in=options['slugs'])

        heroes = list(qs)
        if not heroes:
            self.stdout.write(self.style.WARNING('No heroes need enhancement.'))
            return

        self.stdout.write(f'Enhancing {len(heroes)} hero photo(s)…')

        for hero in heroes:
            self.stdout.write(f'  [{hero.slug}] starting…')
            Legacy.objects.filter(pk=hero.pk).update(photo_enhancement_status='pending')
            try:
                _run_enhancement(hero.pk)
                hero.refresh_from_db()
                if hero.photo_enhancement_status == 'done':
                    self.stdout.write(self.style.SUCCESS(f'  [{hero.slug}] ✓ done'))
                else:
                    self.stdout.write(self.style.ERROR(f'  [{hero.slug}] ✗ failed'))
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f'  [{hero.slug}] ✗ error: {exc}'))
            # Replicate free tier = 6 req/min burst 1; wait between heroes
            time.sleep(12)

        self.stdout.write(self.style.SUCCESS('Enhancement run complete.'))
