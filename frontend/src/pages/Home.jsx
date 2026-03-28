import { useState, useEffect, useCallback } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { fetchLegacies, fetchZones } from '../api';
import { useLang } from '../i18n/LanguageContext';
import LegacyCard from '../components/LegacyCard';
import './Home.css';

const API_BASE = import.meta.env.VITE_API_URL || '';

function FlameIcon() {
  return (
    <svg className="hero-flame" viewBox="0 0 36 56" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M18 2C18 2 5 20 5 32C5 43.6 10.9 52 18 54C25.1 52 31 43.6 31 32C31 20 18 2 18 2Z"
        fill="url(#fg1)" />
      <path d="M18 22C18 22 12 30 12 36C12 40.4 14.7 44 18 45C21.3 44 24 40.4 24 36C24 30 18 22 18 22Z"
        fill="url(#fg2)" />
      <defs>
        <linearGradient id="fg1" x1="18" y1="2" x2="18" y2="54" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#e8c268" />
          <stop offset="100%" stopColor="#a06820" stopOpacity="0.8" />
        </linearGradient>
        <linearGradient id="fg2" x1="18" y1="22" x2="18" y2="45" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#f5ead5" stopOpacity="0.95" />
          <stop offset="100%" stopColor="#e8c268" />
        </linearGradient>
      </defs>
    </svg>
  );
}

function OdaaWatermark() {
  return (
    <svg
      className="hero-odaa-watermark"
      viewBox="0 0 280 230"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <defs>
        <mask id="odaa-mask">
          <ellipse cx="55" cy="110" rx="58" ry="52" fill="white" />
          <ellipse cx="225" cy="110" rx="58" ry="52" fill="white" />
          <ellipse cx="140" cy="80" rx="100" ry="72" fill="white" />
          <ellipse cx="140" cy="40" rx="65" ry="40" fill="white" />
          <ellipse cx="80" cy="55" rx="42" ry="36" fill="white" />
          <ellipse cx="200" cy="55" rx="42" ry="36" fill="white" />
          <rect x="128" y="152" width="24" height="62" rx="6" fill="white" />
          <ellipse cx="140" cy="215" rx="52" ry="8" fill="white" />
        </mask>
      </defs>
      <rect x="0" y="0" width="280" height="230" fill="currentColor" mask="url(#odaa-mask)" />
    </svg>
  );
}

function SkeletonCard() {
  return (
    <div className="skeleton-card" aria-hidden="true">
      <div className="skeleton-photo" />
      <div className="skeleton-body">
        <div className="skeleton-line skeleton-name" />
        <div className="skeleton-line skeleton-occ" />
        <div className="skeleton-line skeleton-text" />
        <div className="skeleton-line skeleton-text short" />
      </div>
    </div>
  );
}

export default function Home() {
  const { t } = useLang();
  const [searchParams, setSearchParams] = useSearchParams();
  const [legacies, setLegacies] = useState([]);
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({ count: 0, next: null, previous: null });
  const [page, setPage] = useState(1);
  const [heroCount, setHeroCount] = useState(null);

  const q = searchParams.get('q') || '';
  const zone = searchParams.get('zone') || '';

  useEffect(() => {
    fetch(`${API_BASE}/api/count/`)
      .then(r => r.json())
      .then(data => setHeroCount(data.approved ?? null))
      .catch(() => {});
  }, []);

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

  const totalPages = pagination.count ? Math.ceil(pagination.count / 9) : 1;

  return (
    <div className="home">
      <section className="hero">
        <div className="hero-glow" aria-hidden="true" />
        <div className="hero-pattern" aria-hidden="true" />
        <OdaaWatermark />
        <div className="container hero-inner">
          <FlameIcon />
          <p className="hero-kicker">{t('hero.kicker')}</p>
          <h1 className="hero-title">{t('hero.title')}</h1>
          <div className="hero-ornament">
            <span className="ornament-line" />
            <span className="ornament-star">✦</span>
            <span className="ornament-line" />
          </div>
          <p className="hero-sub">{t('hero.subtitle')}</p>

          {heroCount !== null && (
            <div className="hero-counter">
              <span className="hero-counter-number">{heroCount.toLocaleString()}</span>
              <span className="hero-counter-label">
                {heroCount === 1 ? 'hero remembered on this wall' : 'heroes remembered on this wall'}
              </span>
            </div>
          )}

          <div className="hero-actions">
            <Link to="/submit" className="btn btn-primary">{t('hero.btn_honor')}</Link>
            <a href="#wall" className="btn btn-outline">{t('hero.btn_explore')}</a>
          </div>
        </div>
      </section>

      <section className="about-band" aria-label="About">
        <div className="container about-band-inner">
          <h2 className="about-band-title">{t('about_band.title')}</h2>
          <p className="about-band-text">{t('about_band.line1')}</p>
          <p className="about-band-text">{t('about_band.line2')}</p>
        </div>
      </section>

      <section className="wall-section" id="wall">
        <div className="container">
          <div className="wall-heading">
            <h2 className="wall-title">{t('wall.title')}</h2>
            <p className="wall-subtitle">{t('wall.subtitle')}</p>
            <div className="wall-ornament">
              <span className="ornament-line-short" />
              <span className="ornament-star-sm">✦</span>
              <span className="ornament-line-short" />
            </div>
          </div>

          <div className="search-row">
            <form className="search-bar" onSubmit={handleSearch}>
              <div className="search-input-wrap">
                <span className="search-icon" aria-hidden="true">🔍</span>
                <input
                  name="q"
                  type="search"
                  className="form-input search-input"
                  placeholder={t('wall.search_placeholder')}
                  defaultValue={q}
                  key={q}
                />
                <button type="submit" className="btn btn-primary search-btn-inline">{t('wall.search_btn')}</button>
              </div>
              <div className="zone-filter-wrap">
                <span className="zone-filter-label">{t('wall.filter_zone')}</span>
                <select name="zone" className="form-select zone-select" defaultValue={zone} key={zone}>
                  <option value="">{t('wall.all_zones')}</option>
                  {zones.map(z => (
                    <option key={z.id} value={z.slug}>{z.name}</option>
                  ))}
                </select>
              </div>
              {(q || zone) && (
                <button type="button" className="btn btn-ghost" onClick={() => setSearchParams({})}>
                  Clear filters
                </button>
              )}
            </form>
            <Link to="/submit" className="btn btn-outline btn-honor">{t('wall.be_first')}</Link>
          </div>
          <p className="search-hint">{t('wall.search_hint')}</p>

          {(q || zone) && (
            <p className="search-result-info">
              {loading ? 'Searching…' : `${legacies.length} ${legacies.length === 1 ? 'life' : 'lives'} found`}
              {q && <> for "<em>{q}</em>"</>}
              {zone && zones.find(z => z.slug === zone) && <> in <em>{zones.find(z => z.slug === zone)?.name}</em></>}
            </p>
          )}

          {loading ? (
            <div className="legacy-grid">
              {Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)}
            </div>
          ) : legacies.length === 0 ? (
            <div className="empty-state">
              <div className="empty-flame">🕯</div>
              <h3>{t('wall.no_lives')}</h3>
              <p>{t('wall.empty_sub')}</p>
              <Link to="/submit" className="btn btn-primary" style={{ marginTop: '2rem' }}>
                {t('wall.be_first')}
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
                    {t('wall.prev')}
                  </button>
                  <span className="page-info">{t('wall.page_of', { page, total: totalPages })}</span>
                  <button className="btn btn-ghost" onClick={() => handlePageChange(page + 1)} disabled={page === totalPages || !pagination.next}>
                    {t('wall.next')}
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
