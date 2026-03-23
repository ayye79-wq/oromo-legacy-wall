import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchLegacy } from '../api';
import './LegacyDetail.css';

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
}

export default function LegacyDetail() {
  const { slug } = useParams();
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
        <span>Loading their story…</span>
      </div>
    );
  }

  if (error === 'not_found') {
    return (
      <div className="detail-error">
        <div className="container">
          <div className="empty-state">
            <div style={{ fontSize: '2rem', marginBottom: '1rem', opacity: 0.3 }}>🕯</div>
            <h3>Story Not Found</h3>
            <p>This legacy may not exist or is still awaiting review.</p>
            <Link to="/" className="btn btn-outline" style={{ marginTop: '2rem' }}>
              Return to the Wall
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
          <div className="alert alert-error">Something went wrong. Please try again.</div>
          <Link to="/" style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>← Return to the Wall</Link>
        </div>
      </div>
    );
  }

  const { full_name, occupation, zone_name, story, photo_url, approved_at } = legacy;

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
          <Link to="/" className="detail-back">← Wall of Remembrance</Link>

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
                Honored on the wall · {formatDate(approved_at)}
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
              <span className="story-orn-label">Their Story</span>
              <span className="story-orn-line" />
            </div>
          </div>
          <div className="detail-story">
            {story.split('\n').filter(p => p.trim()).map((para, i) => (
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
            <h3 className="sidebar-title">In Remembrance</h3>
            <dl className="sidebar-dl">
              <dt>Name</dt>
              <dd>{full_name}</dd>
              {zone_name && (
                <>
                  <dt>Region</dt>
                  <dd>{zone_name}, Oromiyaa</dd>
                </>
              )}
              {approved_at && (
                <>
                  <dt>Honored</dt>
                  <dd>{formatDate(approved_at)}</dd>
                </>
              )}
            </dl>
          </div>

          <div className="sidebar-actions">
            <Link to="/" className="btn btn-ghost sidebar-btn">
              ← Return to the Wall
            </Link>
            <Link to="/submit" className="btn btn-outline sidebar-btn">
              Honor Another Life
            </Link>
          </div>
        </aside>
      </div>
    </div>
  );
}
