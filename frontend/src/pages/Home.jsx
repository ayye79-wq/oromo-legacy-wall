import { useState, useEffect, useCallback } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { fetchLegacies, fetchZones } from '../api';
import LegacyCard from '../components/LegacyCard';
import './Home.css';

export default function Home() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [legacies, setLegacies] = useState([]);
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({ count: 0, next: null, previous: null });
  const [page, setPage] = useState(1);

  const q = searchParams.get('q') || '';
  const zone = searchParams.get('zone') || '';

  const load = useCallback(async (currentPage = 1) => {
    setLoading(true);
    try {
      const data = await fetchLegacies({ q, zone, page: currentPage });
      if (Array.isArray(data)) {
        setLegacies(data);
        setPagination({ count: data.length, next: null, previous: null });
      } else {
        setLegacies(data.results || data);
        setPagination({ count: data.count || 0, next: data.next, previous: data.previous });
      }
    } catch {
      setLegacies([]);
    }
    setLoading(false);
  }, [q, zone]);

  useEffect(() => {
    setPage(1);
    load(1);
  }, [q, zone]);

  useEffect(() => {
    fetchZones().then(data => setZones(Array.isArray(data) ? data : data.results || [])).catch(() => {});
  }, []);

  function handleSearch(e) {
    e.preventDefault();
    const form = e.target;
    const val = form.q.value.trim();
    const zoneVal = form.zone.value;
    const params = {};
    if (val) params.q = val;
    if (zoneVal) params.zone = zoneVal;
    setSearchParams(params);
  }

  function handlePageChange(newPage) {
    setPage(newPage);
    load(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const totalPages = pagination.count ? Math.ceil(pagination.count / 12) : 1;

  return (
    <div className="home">
      <section className="hero">
        <div className="container hero-inner">
          <div className="hero-badge">Digital Memorial Platform</div>
          <h1 className="hero-title">
            Preserving Oromo Lives,<br />
            <span className="hero-highlight">Honoring Their Legacy</span>
          </h1>
          <p className="hero-sub">
            A dignified archive where families and communities document and preserve
            the stories of loved ones — for generations to come.
          </p>
          <div className="hero-actions">
            <Link to="/submit" className="btn btn-primary">Submit a Legacy</Link>
            <a href="#wall" className="btn btn-outline">Explore the Wall</a>
          </div>
        </div>
        <div className="hero-decoration" aria-hidden="true">
          <div className="deco-ring deco-ring-1" />
          <div className="deco-ring deco-ring-2" />
          <div className="deco-ring deco-ring-3" />
        </div>
      </section>

      <section className="wall-section" id="wall">
        <div className="container">
          <div className="wall-header">
            <div>
              <h2 className="wall-title">The Legacy Wall</h2>
              <p className="wall-subtitle">Stories of Oromo individuals, preserved with dignity</p>
            </div>
            <Link to="/submit" className="btn btn-outline btn-sm">+ Add a Legacy</Link>
          </div>

          <form className="search-bar" onSubmit={handleSearch}>
            <div className="search-input-wrap">
              <span className="search-icon" aria-hidden="true">🔍</span>
              <input
                name="q"
                type="search"
                className="form-input search-input"
                placeholder="Search by name or story…"
                defaultValue={q}
                key={q}
              />
            </div>
            <select name="zone" className="form-select zone-select" defaultValue={zone} key={zone}>
              <option value="">All Zones</option>
              {zones.map(z => (
                <option key={z.id} value={z.slug}>{z.name}</option>
              ))}
            </select>
            <button type="submit" className="btn btn-primary">Search</button>
            {(q || zone) && (
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => setSearchParams({})}
              >
                Clear
              </button>
            )}
          </form>

          {(q || zone) && (
            <p className="search-result-info">
              {loading ? 'Searching…' : `${legacies.length} result${legacies.length !== 1 ? 's' : ''} found`}
              {q && <> for "<strong>{q}</strong>"</>}
              {zone && zones.find(z => z.slug === zone) && <> in <strong>{zones.find(z => z.slug === zone)?.name}</strong></>}
            </p>
          )}

          {loading ? (
            <div className="page-loading">
              <div className="spinner" />
              <p>Loading legacies…</p>
            </div>
          ) : legacies.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">✦</div>
              <h3>No legacies found</h3>
              <p>Be the first to share a story.</p>
              <Link to="/submit" className="btn btn-primary" style={{ marginTop: '1.5rem' }}>
                Submit a Legacy
              </Link>
            </div>
          ) : (
            <>
              <div className="legacy-grid">
                {legacies.map(l => <LegacyCard key={l.id} legacy={l} />)}
              </div>

              {totalPages > 1 && (
                <div className="pagination">
                  <button
                    className="btn btn-ghost"
                    onClick={() => handlePageChange(page - 1)}
                    disabled={page === 1}
                  >
                    ← Previous
                  </button>
                  <span className="page-info">Page {page} of {totalPages}</span>
                  <button
                    className="btn btn-ghost"
                    onClick={() => handlePageChange(page + 1)}
                    disabled={page === totalPages || !pagination.next}
                  >
                    Next →
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </section>

      <section className="mission-section">
        <div className="container mission-inner">
          <div className="mission-text">
            <h2>Our Mission</h2>
            <p>
              Oromo Legacy Wall is a permanent, respectful digital monument where families
              and communities can document and preserve the stories of loved ones for future
              generations. Every legacy submitted undergoes a thoughtful review by trusted
              community moderators assigned to each zone of Oromiyaa.
            </p>
          </div>
          <div className="mission-stats">
            <div className="stat">
              <span className="stat-icon">✦</span>
              <span className="stat-label">Community Driven</span>
            </div>
            <div className="stat">
              <span className="stat-icon">🛡</span>
              <span className="stat-label">Zone-Based Moderation</span>
            </div>
            <div className="stat">
              <span className="stat-icon">📜</span>
              <span className="stat-label">Permanent Archive</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
