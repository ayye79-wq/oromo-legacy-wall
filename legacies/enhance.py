"""
AI photo enhancement via Replicate (GFPGAN face restoration).
Called as a background thread after a new Legacy is saved with a photo.
"""
import logging
import os
import time
import threading
import urllib.request

logger = logging.getLogger(__name__)

GFPGAN_VERSION = '0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c'
_MAX_RETRIES = 3
_RETRY_WAIT = 15  # seconds between retries when rate-limited


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

        output = None
        last_exc = None
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                output = replicate.run(
                    f'tencentarc/gfpgan:{GFPGAN_VERSION}',
                    input={
                        'img': photo_url,
                        'version': 'v1.4',
                        'scale': 2,
                    },
                )
                break
            except Exception as exc:
                last_exc = exc
                err_str = str(exc)
                if '429' in err_str or 'throttled' in err_str.lower():
                    logger.warning('Rate limited on attempt %d/%d for pk=%d, waiting %ds…',
                                   attempt, _MAX_RETRIES, legacy_pk, _RETRY_WAIT)
                    time.sleep(_RETRY_WAIT)
                else:
                    raise

        if output is None:
            raise last_exc

        # output is a URL string pointing to the enhanced image
        enhanced_url = output if isinstance(output, str) else str(output)
        logger.info('Enhancement done for pk=%d', legacy_pk)

        # Validate URL before downloading — must be HTTPS from Replicate's CDN
        from urllib.parse import urlparse as _urlparse
        _parsed = _urlparse(enhanced_url)
        if _parsed.scheme != 'https' or not _parsed.netloc.endswith(('replicate.delivery', 'replicate.com', 'pbxt.replicate.delivery')):
            raise ValueError(f'Unexpected enhancement URL origin: {_parsed.netloc}')

        # Download enhanced image
        req = urllib.request.Request(enhanced_url, headers={'User-Agent': 'OromoLegacyWall/1.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
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
