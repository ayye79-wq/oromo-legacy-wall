import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LanguageProvider } from './i18n/LanguageContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import SubmitLegacy from './pages/SubmitLegacy';
import LegacyDetail from './pages/LegacyDetail';

function NotFound() {
  return (
    <div style={{ padding: '5rem 1.5rem', textAlign: 'center', flex: 1 }}>
      <div style={{ fontSize: '2rem', color: 'var(--accent)', marginBottom: '1rem' }}>✦</div>
      <h2 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Page Not Found</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        The page you're looking for doesn't exist.
      </p>
      <a href="/" className="btn btn-primary">Return Home</a>
    </div>
  );
}

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Navbar />
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/submit" element={<SubmitLegacy />} />
            <Route path="/legacy/:slug" element={<LegacyDetail />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
