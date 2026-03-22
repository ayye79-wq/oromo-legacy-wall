import { useState, useEffect, useCallback } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { fetchLegacies, fetchZones } from '../api';
import LegacyCard from '../components/LegacyCard';
import './Home.css';

function FlameIcon() {
  return (
    <svg className="hero-flame" viewBox="0 0 36 56" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M18 2C18 2 5 20 5 32C5 43.6 10.9 52 18 54C25.1 52 31 43.6 31 32C31 20 18 2 18 2Z"
        fill="url(#fg1)" />
      <path d="M18 22C18 22 12 30 12 36C12 40.4 14.7 44 18 45C21.3 44 24 40.4 24 36C24 30 18 22 18 22Z"
        fill="url(#fg2)" />
      <defs>
        <linearGradient id="fg1" x1="18" y1="2" x2="18" y2="54" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#ddb06a" />
          <stop offset="100%" stopColor="#a06820" stopOpacity="0.8" />
        </linearGradient>
        <linearGradient id="fg2" x1="18" y1="22" x2="18" y2="45" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#f5ead5" stopOpacity="0.95" />
          <stop offset="100%" stopColor="#ddb06a" />
        </linearGradient>
      </defs>
    </svg>
  );
}

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
        <div className="hero-glow" aria-hidden="true" />
        <div className="container hero-inner">
          <FlameIcon />
          <p className="hero-kicker">In Remembrance</p>
          <h1 className="hero-title">
            Their Stories Live On
          </h1>
          <div className="hero-ornament">
            <span className="ornament-line" />
            <span className="ornament-star">✦</span>
            <span className="ornament-line" />
          </div>
          <p className="hero-sub">
            A sacred space where Oromo families and communities come together
            to document, preserve, and honor the lives of those who shaped
            our world — so their memory endures for all generations.
          </p>
          <div className="hero-actions">
            <Link to="/submit" className="btn btn-primary">Honor a Life</Link>
            <a href="#wall" className="btn btn-outline">Enter the Memorial Wall</a>
          </div>
        </div>
      </section>

      <section className="wall-section" id="wall">
        <div className="container">
          <div className="wall-heading">
            <h2 className="wall-title">Wall of Remembrance</h2>
            <p className="wall-subtitle">Each name here was a life lived, a story worth telling</p>
            <div className="wall-ornament">
              <span className="ornament-line-short" />
              <span className="ornament-star-sm">✦</span>
              <span className="ornament-line-short" />
            </div>
          </div>

          <div className="search-row">
            <form className="search-bar" onSubmit={handleSearch}>
              <div className="search-input-wrap">
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
                <option value="">All Zones of Oromiyaa</option>
                {zones.map(z => (
                  <option key={z.id} value={z.slug}>{z.name}</option>
                ))}
              </select>
              <button type="submit" className="btn btn-primary">Search</button>
              {(q || zone) && (
                <button type="button" className="btn btn-ghost" onClick={() => setSearchParams({})}>
                  Clear
                </button>
              )}
            </form>
            <Link to="/submit" className="btn btn-outline btn-honor">Honor a Life</Link>
          </div>

          {(q || zone) && (
            <p className="search-result-info">
              {loading ? 'Searching…' : `${legacies.length} ${legacies.length === 1 ? 'life' : 'lives'} found`}
              {q && <> for "<em>{q}</em>"</>}
              {zone && zones.find(z => z.slug === zone) && <> in <em>{zones.find(z => z.slug === zone)?.name}</em></>}
            </p>
          )}

          {loading ? (
            <div className="page-loading">
              <div className="spinner" />
              <span>Gathering stories…</span>
            </div>
          ) : legacies.length === 0 ? (
            <div className="empty-state">
              <div className="empty-flame">🕯</div>
              <h3>No lives have been honored yet</h3>
              <p>Be the first to preserve a story on this wall.</p>
              <Link to="/submit" className="btn btn-primary" style={{ marginTop: '2rem' }}>
                Honor a Life
              </Link>
            </div>
          ) : (
            <>
              <div className="legacy-grid">
                {legacies.map(l => <LegacyCard key={l.id} legacy={l} />)}
              </div>

              {totalPages > 1 && (
                <div className="pagination">
                  <button className="btn btn-ghost" onClick={() => handlePageChange(page - 1)} disabled={page === 1}>
                    ← Previous
                  </button>
                  <span className="page-info">Page {page} of {totalPages}</span>
                  <button className="btn btn-ghost" onClick={() => handlePageChange(page + 1)} disabled={page === totalPages || !pagination.next}>
                    Next →
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </section>

      <section className="about-section">
        <div className="container about-inner">
          <div className="about-text">
            <h2 className="about-title">A Permanent Place of Memory</h2>
            <p>
              The Oromo Legacy Wall is a living archive — a digital monument built to ensure
              that the stories of Oromo individuals are never forgotten. Every submission is
              reviewed with care by trusted community moderators from each zone of Oromiyaa,
              preserving authenticity, dignity, and cultural truth.
            </p>
            <p>
              This is not just a website. It is a place of mourning, of pride, and of
              remembrance — where future generations will come to learn who came before them.
            </p>
          </div>
          <div className="about-pillars">
            <div className="pillar">
              <span className="pillar-icon">🕯</span>
              <h3>Dignity First</h3>
              <p>Every life honored here is treated with the respect it deserves.</p>
            </div>
            <div className="pillar">
              <span className="pillar-icon">🌍</span>
              <h3>Community Verified</h3>
              <p>Zone moderators from Oromiyaa ensure authenticity and cultural care.</p>
            </div>
            <div className="pillar">
              <span className="pillar-icon">📜</span>
              <h3>Forever Preserved</h3>
              <p>Stories submitted here are kept for generations yet to come.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
