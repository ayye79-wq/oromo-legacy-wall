import './Footer.css';

function OdaaSmall() {
  return (
    <svg
      className="footer-odaa"
      viewBox="0 0 120 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Odaa tree — symbol of the Gadaa system"
    >
      <ellipse cx="24" cy="48" rx="26" ry="23" fill="currentColor" />
      <ellipse cx="96" cy="48" rx="26" ry="23" fill="currentColor" />
      <ellipse cx="60" cy="34" rx="44" ry="32" fill="currentColor" />
      <ellipse cx="60" cy="16" rx="28" ry="18" fill="currentColor" />
      <rect x="54" y="64" width="12" height="28" rx="3" fill="currentColor" />
      <ellipse cx="60" cy="93" rx="24" ry="4" fill="currentColor" opacity="0.4" />
    </svg>
  );
}

export default function Footer() {
  return (
    <footer className="footer">
      <div className="gadaa-stripe" aria-hidden="true">
        <span className="stripe-red" />
        <span className="stripe-white" />
        <span className="stripe-green" />
      </div>

      <div className="footer-ornament" aria-hidden="true">
        <span className="footer-orn-line" />
        <OdaaSmall />
        <span className="footer-orn-line" />
      </div>

      <div className="container footer-inner">
        <div className="footer-brand">Oromo Legacy Wall</div>
        <p className="footer-tagline">
          "Until the lion learns to write, every story will glorify the hunter."
        </p>
        <p className="footer-mission">
          A permanent digital memorial honoring Oromo lives — built by the community,
          for all generations.
        </p>
        <p className="footer-odaa-label">
          Beneath the Odaa, no voice is ever forgotten.
        </p>
      </div>
    </footer>
  );
}
