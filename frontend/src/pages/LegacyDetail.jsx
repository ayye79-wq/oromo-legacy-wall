import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
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

export default function LegacyDetail() {
  const { slug } = useParams();
  const { lang, t } = useLang();
  const [legacy, setLegacy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchLegacy(slug)
      .then(data => setLegacy(data))
      .catch(err => setError(err.status === 404 ? 'not_found' : 'error'))
      .finally(() => setLoading(false));
  }, [slug]);

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

  const { full_name, occupation, zone_name, story, story_en, story_om, original_language, photo_url, approved_at } = legacy;

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

  return (
    <div className="detail-page">
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
              <img src={photo_url} alt={full_name} className="detail-portrait" />
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
