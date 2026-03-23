import { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { fetchLegacy } from '../api';
import { useLang } from '../i18n/LanguageContext';
import TributeSection from '../components/TributeSection';
import './LegacyDetail.css';

function formatDate(dateStr, lang) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString(lang === 'om' ? 'en-US' : 'en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });
}

function Lightbox({ src, name, onClose }) {
  useEffect(() => {
    function onKey(e) { if (e.key === 'Escape') onClose(); }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [onClose]);

  return (
    <div className="lightbox-overlay" onClick={onClose} role="dialog" aria-modal="true" aria-label={`Portrait of ${name}`}>
      <button className="lightbox-close" onClick={onClose} aria-label="Close">✕</button>
      <div className="lightbox-inner" onClick={e => e.stopPropagation()}>
        <img src={src} alt={name} className="lightbox-img" />
        <p className="lightbox-caption">{name}</p>
      </div>
    </div>
  );
}

export default function LegacyDetail() {
  const { slug } = useParams();
  const { lang, t } = useLang();
  const [legacy, setLegacy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lightboxOpen, setLightboxOpen] = useState(false);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchLegacy(slug)
      .then(data => setLegacy(data))
      .catch(err => setError(err.status === 404 ? 'not_found' : 'error'))
      .finally(() => setLoading(false));
  }, [slug]);

  const closeLightbox = useCallback(() => setLightboxOpen(false), []);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" />
        <span>{t('detail.loading')}</span>
      </div>
    );
  }

  if (error === 'not_found') {
    return (
      <div className="detail-error">
        <div className="container">
          <div className="empty-state">
            <div style={{ fontSize: '2rem', marginBottom: '1rem', opacity: 0.3 }}>🕯</div>
            <h3>{t('detail.not_found')}</h3>
            <p>{t('detail.not_found_sub')}</p>
            <Link to="/" className="btn btn-outline" style={{ marginTop: '2rem' }}>
              {t('detail.return_wall')}
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="detail-error">
        <div className="container">
          <div className="alert alert-error">{t('detail.error')}</div>
          <Link to="/" style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            {t('detail.back')}
          </Link>
        </div>
      </div>
    );
  }

  const {
    full_name, occupation, relationship_to_person, zone_name,
    story, story_en, story_om, original_language, photo_url, approved_at,
  } = legacy;

  function resolveStory() {
    if (lang === 'om') {
      if (story_om && story_om.trim()) return { text: story_om, note: null };
      const fallback = story_en || story || '';
      return { text: fallback, note: t('detail.fallback_note') };
    }
    if (story_en && story_en.trim()) return { text: story_en, note: null };
    if (original_language === 'om' && story_om && story_om.trim()) {
      return { text: story_om, note: t('detail.story_in_om') };
    }
    return { text: story || '', note: null };
  }

  const { text: storyText, note: storyNote } = resolveStory();

  const pageTitle = `${full_name} — Oromo Legacy Wall`;
  const pageDesc = (story_en || story || '').slice(0, 200).trim();
  const canonicalUrl = `${window.location.origin}/legacy/${slug}`;
  const absolutePhoto = photo_url
    ? (photo_url.startsWith('http') ? photo_url : `${window.location.origin}${photo_url}`)
    : null;

  return (
    <div className="detail-page">
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDesc} />
        <link rel="canonical" href={canonicalUrl} />

        <meta property="og:type" content="article" />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDesc} />
        <meta property="og:url" content={canonicalUrl} />
        <meta property="og:site_name" content="Oromo Legacy Wall" />
        {absolutePhoto && <meta property="og:image" content={absolutePhoto} />}
        {absolutePhoto && <meta property="og:image:alt" content={`Portrait of ${full_name}`} />}

        <meta name="twitter:card" content={absolutePhoto ? 'summary_large_image' : 'summary'} />
        <meta name="twitter:title" content={pageTitle} />
        <meta name="twitter:description" content={pageDesc} />
        {absolutePhoto && <meta name="twitter:image" content={absolutePhoto} />}
      </Helmet>

      {lightboxOpen && photo_url && (
        <Lightbox src={photo_url} name={full_name} onClose={closeLightbox} />
      )}

      <div className="detail-hero">
        {photo_url && (
          <div
            className="detail-photo-bg"
            style={{ backgroundImage: `url(${photo_url})` }}
            aria-hidden="true"
          />
        )}
        <div className="detail-hero-overlay" aria-hidden="true" />
        <div className="container detail-hero-inner">
          <Link to="/" className="detail-back">{t('detail.back')}</Link>

          <div className="detail-portrait-wrap">
            {photo_url ? (
              <button
                className="detail-portrait-btn"
                onClick={() => setLightboxOpen(true)}
                title="Click to enlarge portrait"
                aria-label={`Enlarge portrait of ${full_name}`}
              >
                <img src={photo_url} alt={full_name} className="detail-portrait" />
                <span className="portrait-enlarge-hint" aria-hidden="true">⤢</span>
              </button>
            ) : (
              <div className="detail-portrait-placeholder" aria-hidden="true">
                <span>{full_name.charAt(0)}</span>
              </div>
            )}
          </div>

          <div className="detail-meta">
            {zone_name && <span className="tag tag-zone">{zone_name}</span>}
            <h1 className="detail-name">{full_name}</h1>
            {occupation && (
              <p className="detail-occupation">{occupation}</p>
            )}
            {approved_at && (
              <time className="detail-date" dateTime={approved_at}>
                {t('detail.honored_on')} · {formatDate(approved_at, lang)}
              </time>
            )}
          </div>
        </div>
      </div>

      <div className="container detail-body">
        <article className="detail-story-wrap">
          <div className="story-intro">
            <div className="story-ornament">
              <span className="story-orn-line" />
              <span className="story-orn-label">{t('detail.their_story')}</span>
              <span className="story-orn-line" />
            </div>
          </div>

          {storyNote && (
            <p className="story-lang-note">{storyNote}</p>
          )}

          <div className="detail-story">
            {storyText.split('\n').filter(p => p.trim()).map((para, i) => (
              <p key={i}>{para}</p>
            ))}
          </div>
          <div className="story-close">
            <span className="story-orn-line" />
            <span style={{ color: 'var(--accent)', fontSize: '0.7rem', opacity: 0.5 }}>✦</span>
            <span className="story-orn-line" />
          </div>
        </article>

        <aside className="detail-sidebar">
          <div className="sidebar-card">
            <h3 className="sidebar-title">{t('detail.in_remembrance')}</h3>
            <dl className="sidebar-dl">
              <dt>{t('detail.name')}</dt>
              <dd>{full_name}</dd>
              {occupation && (
                <>
                  <dt>Occupation</dt>
                  <dd>{occupation}</dd>
                </>
              )}
              {relationship_to_person && (
                <>
                  <dt>Submitted by</dt>
                  <dd>{relationship_to_person}</dd>
                </>
              )}
              {zone_name && (
                <>
                  <dt>{t('detail.region')}</dt>
                  <dd>{zone_name}, Oromiyaa</dd>
                </>
              )}
              {approved_at && (
                <>
                  <dt>{t('detail.honored')}</dt>
                  <dd>{formatDate(approved_at, lang)}</dd>
                </>
              )}
            </dl>
          </div>

          <div className="sidebar-actions">
            <Link to="/" className="btn btn-ghost sidebar-btn">
              {t('detail.return')}
            </Link>
            <Link to="/submit" className="btn btn-outline sidebar-btn">
              {t('detail.honor_another')}
            </Link>
          </div>
        </aside>
      </div>

      <TributeSection slug={slug} />
    </div>
  );
}
