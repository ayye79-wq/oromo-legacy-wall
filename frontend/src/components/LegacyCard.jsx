import { Link } from 'react-router-dom';
import './LegacyCard.css';

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

export default function LegacyCard({ legacy }) {
  const { full_name, slug, zone_name, story, photo_url, approved_at } = legacy;

  return (
    <Link to={`/legacy/${slug}`} className="legacy-card">
      <div className="card-photo-wrap">
        {photo_url ? (
          <img src={photo_url} alt={full_name} className="card-photo" loading="lazy" />
        ) : (
          <div className="card-photo-placeholder">
            <span>{full_name.charAt(0)}</span>
          </div>
        )}
      </div>
      <div className="card-body">
        <h3 className="card-name">{full_name}</h3>
        {zone_name && (
          <span className="tag tag-zone card-zone">{zone_name}</span>
        )}
        <p className="card-story">{story}</p>
        {approved_at && (
          <time className="card-date" dateTime={approved_at}>
            {formatDate(approved_at)}
          </time>
        )}
      </div>
      <div className="card-footer">
        <span className="card-read-more">Read Full Legacy →</span>
      </div>
    </Link>
  );
}
