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
        <p>Loading legacy…</p>
      </div>
    );
  }

  if (error === 'not_found') {
    return (
      <div className="detail-error">
        <div className="container">
          <div className="empty-state">
            <div style={{ fontSize: '2.5rem', marginBottom: '1rem', opacity: 0.4 }}>✦</div>
            <h3>Legacy Not Found</h3>
            <p>This legacy may not exist or is still pending review.</p>
            <Link to="/" className="btn btn-primary" style={{ marginTop: '1.5rem' }}>
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
          <Link to="/">← Back to the Wall</Link>
        </div>
      </div>
    );
  }

  const { full_name, zone_name, story, photo_url, approved_at, created_at } = legacy;

  return (
    <div className="detail-page">
      <div className="detail-hero">
        {photo_url && (
          <div className="detail-photo-bg" style={{ backgroundImage: `url(${photo_url})` }} aria-hidden="true" />
        )}
        <div className="detail-hero-overlay" aria-hidden="true" />
        <div className="container detail-hero-inner">
          <Link to="/" className="detail-back">← Back to the Wall</Link>
          <div className={`detail-photo-wrap ${!photo_url ? 'no-photo' : ''}`}>
            {photo_url ? (
              <img src={photo_url} alt={full_name} className="detail-photo" />
            ) : (
              <div className="detail-photo-placeholder">
                {full_name.charAt(0)}
              </div>
            )}
          </div>
          <div className="detail-meta">
            {zone_name && <span className="tag tag-zone">{zone_name}</span>}
            <h1 className="detail-name">{full_name}</h1>
            {approved_at && (
              <time className="detail-date" dateTime={approved_at}>
                Honored on {formatDate(approved_at)}
              </time>
            )}
          </div>
        </div>
      </div>

      <div className="container detail-body">
        <div className="detail-story-wrap">
          <div className="story-header">
            <span className="story-divider">✦ Their Story ✦</span>
          </div>
          <div className="detail-story">
            {story.split('\n').filter(Boolean).map((para, i) => (
              <p key={i}>{para}</p>
            ))}
          </div>
        </div>

        <div className="detail-sidebar">
          <div className="sidebar-card">
            <h3>About This Legacy</h3>
            <dl>
              <dt>Name</dt>
              <dd>{full_name}</dd>
              {zone_name && (
                <>
                  <dt>Zone</dt>
                  <dd>{zone_name}</dd>
                </>
              )}
              {approved_at && (
                <>
                  <dt>Added to Wall</dt>
                  <dd>{formatDate(approved_at)}</dd>
                </>
              )}
            </dl>
          </div>

          <div className="sidebar-actions">
            <Link to="/" className="btn btn-ghost" style={{ width: '100%', justifyContent: 'center' }}>
              ← All Legacies
            </Link>
            <Link to="/submit" className="btn btn-outline" style={{ width: '100%', justifyContent: 'center' }}>
              Submit a Legacy
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
