import { Link } from 'react-router-dom';
import { useLang } from '../i18n/LanguageContext';
import './About.css';

export default function About() {
  const { t } = useLang();

  return (
    <div className="about-page">
      <section className="about-hero">
        <div className="about-hero-glow" aria-hidden="true" />
        <div className="container about-hero-inner">
          <p className="about-kicker">{t('about.kicker')}</p>
          <h1 className="about-title">{t('about.title')}</h1>
          <div className="hero-ornament">
            <span className="ornament-line" />
            <span className="ornament-star">✦</span>
            <span className="ornament-line" />
          </div>
        </div>
      </section>

      <section className="about-body">
        <div className="container about-content">
          <p className="about-para">{t('about.p1')}</p>
          <p className="about-para">{t('about.p2')}</p>
          <p className="about-para">{t('about.p3')}</p>
          <p className="about-para">{t('about.p4')}</p>
          <p className="about-para">{t('about.p5')}</p>

          <div className="about-divider" aria-hidden="true">
            <span className="ornament-line-short" />
            <span className="ornament-star-sm">✦</span>
            <span className="ornament-line-short" />
          </div>

          <div className="about-actions">
            <Link to="/" className="btn btn-primary">{t('about.btn_wall')}</Link>
            <Link to="/submit" className="btn btn-outline">{t('about.btn_honor')}</Link>
          </div>
        </div>
      </section>
    </div>
  );
}
