import { Link } from 'react-router-dom';
import './LegacyCard.css';

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
}

function PersonSilhouette() {
  return (
    <svg
      className="card-silhouette"
      viewBox="0 0 120 140"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <circle cx="60" cy="42" r="26" fill="currentColor" />
      <path
        d="M10 130 C10 100 28 84 60 84 C92 84 110 100 110 130 Z"
        fill="currentColor"
      />
    </svg>
  );
}

export default function LegacyCard({ legacy }) {
  const { full_name, occupation, slug, zone_name, story_preview, photo_url, approved_at } = legacy;

  return (
    <Link to={`/legacy/${slug}`} className="legacy-card">
      <div className="card-top-border" aria-hidden="true" />
      <div className="card-photo-wrap">
        {photo_url ? (
          <img src={photo_url} alt={full_name} className="card-photo" loading="lazy" />
        ) : (
          <div className="card-photo-placeholder" aria-hidden="true">
            <PersonSilhouette />
          </div>
        )}
      </div>

      <div className="card-body">
        <h3 className="card-name">{full_name}</h3>

        {occupation && (
          <p className="card-occupation">{occupation}</p>
        )}

        {zone_name && (
          <span className="tag tag-zone card-zone">{zone_name}</span>
        )}

        {!occupation && story_preview && (
          <p className="card-story">{story_preview}</p>
        )}

        {approved_at && (
          <time className="card-date" dateTime={approved_at}>
            Remembered · {formatDate(approved_at)}
          </time>
        )}
      </div>

      <div className="card-footer">
        <span className="card-read-more">Read Their Story →</span>
      </div>
    </Link>
  );
}
