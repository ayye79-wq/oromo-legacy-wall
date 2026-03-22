import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div className="footer-brand">
          <span className="footer-icon">✦</span>
          <span>Oromo Legacy Wall</span>
        </div>
        <p className="footer-tagline">
          Preserving the stories of Oromo individuals for generations to come.
        </p>
        <p className="footer-copy">
          A community-driven digital memorial platform.
        </p>
      </div>
    </footer>
  );
}
