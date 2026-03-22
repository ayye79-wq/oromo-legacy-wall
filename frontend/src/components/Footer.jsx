import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-ornament" aria-hidden="true">
        <span className="footer-orn-line" />
        <span className="footer-orn-star">✦</span>
        <span className="footer-orn-line" />
      </div>
      <div className="container footer-inner">
        <div className="footer-candle" aria-hidden="true">🕯</div>
        <div className="footer-brand">Oromo Legacy Wall</div>
        <p className="footer-tagline">
          "Until the lion learns to write, every story will glorify the hunter."
        </p>
        <p className="footer-mission">
          A permanent digital memorial honoring Oromo lives — built by the community,
          for all generations.
        </p>
      </div>
    </footer>
  );
}
