"""
AI photo enhancement via Replicate (GFPGAN face restoration).
Called as a background thread after a new Legacy is saved with a photo.
"""
import io
import logging
import os
import threading
import urllib.request

logger = logging.getLogger(__name__)


def _run_enhancement(legacy_pk: int) -> None:
    """Blocking enhancement — runs in a daemon thread."""
    try:
        import replicate
        from django.core.files.base import ContentFile
        from .models import Legacy

        legacy = Legacy.objects.select_related().get(pk=legacy_pk)

        if not legacy.photo:
            return

        # Build the absolute photo URL for Replicate
        photo_url = legacy.photo.url
        if not photo_url.startswith('http'):
            r2_pub = os.environ.get('R2_PUBLIC_URL', '').rstrip('/')
            if r2_pub:
                if not r2_pub.startswith('http'):
                    r2_pub = f'https://{r2_pub}'
                photo_url = f'{r2_pub}/{legacy.photo.name}'
            else:
                logger.warning('Photo URL is relative and R2_PUBLIC_URL is not set; skipping enhancement.')
                Legacy.objects.filter(pk=legacy_pk).update(photo_enhancement_status='failed')
                return

        logger.info('Enhancing photo for legacy %s (pk=%d) …', legacy.slug, legacy_pk)

        output = replicate.run(
            'tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355f829a539ad21ef2cde5f8c0e5421a',
            input={
                'img': photo_url,
                'version': 'v1.4',
                'scale': 2,
            },
        )

        # output is a URL string pointing to the enhanced image
        enhanced_url = output if isinstance(output, str) else str(output)
        logger.info('Enhancement done for pk=%d, URL=%s', legacy_pk, enhanced_url)

        # Download enhanced image
        with urllib.request.urlopen(enhanced_url, timeout=60) as resp:
            img_bytes = resp.read()

        enhanced_name = f'{legacy.slug}_enhanced.jpg'
        legacy_fresh = Legacy.objects.get(pk=legacy_pk)
        legacy_fresh.photo_enhanced.save(
            enhanced_name,
            ContentFile(img_bytes),
            save=False,
        )
        Legacy.objects.filter(pk=legacy_pk).update(
            photo_enhanced=legacy_fresh.photo_enhanced.name,
            photo_enhancement_status='done',
        )
        logger.info('Enhancement saved for pk=%d as %s', legacy_pk, enhanced_name)

    except Exception as exc:
        logger.error('Enhancement failed for legacy pk=%d: %s', legacy_pk, exc, exc_info=True)
        try:
            from .models import Legacy
            Legacy.objects.filter(pk=legacy_pk).update(photo_enhancement_status='failed')
        except Exception:
            pass


def enhance_photo_async(legacy_pk: int) -> None:
    """Fire-and-forget: run enhancement in a background daemon thread."""
    t = threading.Thread(target=_run_enhancement, args=(legacy_pk,), daemon=True)
    t.start()
