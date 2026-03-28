import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLang } from '../i18n/LanguageContext';
import './Navbar.css';

function OdaaNavIcon() {
  return (
    <svg
      className="brand-odaa"
      viewBox="0 0 56 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <ellipse cx="11" cy="23" rx="12" ry="11" fill="currentColor" />
      <ellipse cx="45" cy="23" rx="12" ry="11" fill="currentColor" />
      <ellipse cx="28" cy="16" rx="22" ry="16" fill="currentColor" />
      <ellipse cx="28" cy="7" rx="14" ry="9" fill="currentColor" />
      <rect x="25" y="31" width="6" height="13" rx="2" fill="currentColor" />
      <ellipse cx="28" cy="44" rx="12" ry="2.5" fill="currentColor" opacity="0.4" />
    </svg>
  );
}

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();
  const { lang, setLang, t } = useLang();

  const links = [
    { to: '/', label: t('nav.wall') },
    { to: '/submit', label: t('nav.honor') },
    { to: '/about', label: t('nav.about') },
  ];

  return (
    <nav className="navbar">
      <div className="gadaa-navbar-stripe" aria-hidden="true" />
      <div className="container navbar-inner">
        <Link to="/" className="navbar-brand" onClick={() => setOpen(false)}>
          <OdaaNavIcon />
          <span className="brand-text">Oromo Legacy Wall</span>
        </Link>

        <button
          className="navbar-toggle"
          onClick={() => setOpen(o => !o)}
          aria-label="Toggle menu"
        >
          <span className={`hamburger ${open ? 'open' : ''}`} />
        </button>

        <ul className={`navbar-links ${open ? 'open' : ''}`}>
          {links.map(({ to, label }) => (
            <li key={to}>
              <Link
                to={to}
                className={`nav-link ${pathname === to ? 'active' : ''}`}
                onClick={() => setOpen(false)}
              >
                {label}
              </Link>
            </li>
          ))}
          <li className="lang-toggle-li">
            <div className="lang-toggle" role="group" aria-label="Language">
              <button
                className={`lang-btn ${lang === 'en' ? 'active' : ''}`}
                onClick={() => setLang('en')}
                aria-pressed={lang === 'en'}
              >
                EN
              </button>
              <span className="lang-sep" aria-hidden="true">|</span>
              <button
                className={`lang-btn ${lang === 'om' ? 'active' : ''}`}
                onClick={() => setLang('om')}
                aria-pressed={lang === 'om'}
              >
                AO
              </button>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  );
}
