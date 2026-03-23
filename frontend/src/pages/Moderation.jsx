import { useState, useEffect } from 'react';
import './Moderation.css';

const API_BASE = import.meta.env.VITE_API_URL || '';

function formatDate(s) {
  if (!s) return '';
  return new Date(s).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  });
}

export default function Moderation() {
  const [secret, setSecret] = useState(() => sessionStorage.getItem('mod_secret') || '');
  const [inputSecret, setInputSecret] = useState('');
  const [authError, setAuthError] = useState('');
  const [authed, setAuthed] = useState(false);
  const [pending, setPending] = useState([]);
  const [count, setCount] = useState(0);
  const [loadingList, setLoadingList] = useState(false);
  const [actionLoading, setActionLoading] = useState({});
  const [toast, setToast] = useState(null);

  function showToast(msg, type = 'success') {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3500);
  }

  async function fetchPending(s) {
    setLoadingList(true);
    try {
      const res = await fetch(`${API_BASE}/api/mod/pending/`, {
        headers: { Authorization: `Bearer ${s}` },
      });
      if (res.status === 401) {
        setAuthed(false);
        setAuthError('Incorrect password. Please try again.');
        sessionStorage.removeItem('mod_secret');
        setSecret('');
        return;
      }
      const data = await res.json();
      setPending(data.results || []);
      setCount(data.count || 0);
      setAuthed(true);
      sessionStorage.setItem('mod_secret', s);
    } catch {
      setAuthError('Could not connect. Please try again.');
    }
    setLoadingList(false);
  }

  useEffect(() => {
    if (secret) fetchPending(secret);
  }, []);

  function handleLogin(e) {
    e.preventDefault();
    setAuthError('');
    setSecret(inputSecret);
    fetchPending(inputSecret);
  }

  async function doAction(id, action) {
    setActionLoading(a => ({ ...a, [id]: action }));
    try {
      const res = await fetch(`${API_BASE}/api/mod/${id}/${action}/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${secret}` },
      });
      if (res.ok) {
        setPending(p => p.filter(x => x.id !== id));
        setCount(c => c - 1);
        showToast(action === 'approve' ? 'Approved and published.' : 'Submission rejected.');
      } else {
        showToast('Action failed. Please try again.', 'error');
      }
    } catch {
      showToast('Network error.', 'error');
    }
    setActionLoading(a => ({ ...a, [id]: null }));
  }

  function handleLogout() {
    sessionStorage.removeItem('mod_secret');
    setSecret('');
    setAuthed(false);
    setPending([]);
    setInputSecret('');
  }

  if (!authed) {
    return (
      <div className="mod-page">
        <div className="mod-login-wrap">
          <div className="mod-login-card">
            <div className="mod-login-icon" aria-hidden="true">🛡️</div>
            <h1 className="mod-login-title">Moderation Dashboard</h1>
            <p className="mod-login-sub">Enter the moderation password to continue.</p>
            {authError && <div className="mod-alert mod-alert-error">{authError}</div>}
            <form onSubmit={handleLogin} className="mod-login-form">
              <input
                type="password"
                className="mod-input"
                placeholder="Moderation password"
                value={inputSecret}
                onChange={e => setInputSecret(e.target.value)}
                autoFocus
                required
              />
              <button type="submit" className="mod-btn mod-btn-primary">
                Enter Dashboard
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mod-page">
      {toast && (
        <div className={`mod-toast mod-toast-${toast.type}`}>{toast.msg}</div>
      )}

      <div className="mod-header">
        <div className="mod-header-inner">
          <div>
            <h1 className="mod-title">Moderation Dashboard</h1>
            <p className="mod-subtitle">
              {loadingList ? 'Loading…' : `${count} submission${count !== 1 ? 's' : ''} awaiting review`}
            </p>
          </div>
          <div className="mod-header-actions">
            <button className="mod-btn mod-btn-ghost" onClick={() => fetchPending(secret)}>
              ↻ Refresh
            </button>
            <button className="mod-btn mod-btn-ghost" onClick={handleLogout}>
              Log out
            </button>
          </div>
        </div>
      </div>

      <div className="mod-body">
        {loadingList ? (
          <div className="mod-loading">
            <div className="mod-spinner" />
            <span>Loading submissions…</span>
          </div>
        ) : pending.length === 0 ? (
          <div className="mod-empty">
            <span aria-hidden="true">✦</span>
            <h2>All clear</h2>
            <p>No submissions are waiting for review right now.</p>
          </div>
        ) : (
          <div className="mod-grid">
            {pending.map(item => (
              <div key={item.id} className="mod-card">
                <div className="mod-card-top">
                  {item.photo_url && (
                    <img
                      src={item.photo_url.startsWith('http') ? item.photo_url : `${API_BASE}${item.photo_url}`}
                      alt={item.full_name}
                      className="mod-card-photo"
                    />
                  )}
                  <div className="mod-card-info">
                    <div className="mod-card-zone">{item.zone_name}</div>
                    <h2 className="mod-card-name">{item.full_name}</h2>
                    {item.occupation && <p className="mod-card-occ">{item.occupation}</p>}
                    {item.relationship_to_person && (
                      <p className="mod-card-rel">Submitted by: {item.relationship_to_person}</p>
                    )}
                    <p className="mod-card-date">Received {formatDate(item.created_at)}</p>
                    <p className="mod-card-lang">
                      Language: <strong>{item.original_language === 'om' ? 'Afaan Oromo' : 'English'}</strong>
                    </p>
                  </div>
                </div>

                <div className="mod-card-story">
                  {(item.story_en || item.story || '').split('\n').filter(p => p.trim()).slice(0, 6).map((para, i) => (
                    <p key={i}>{para}</p>
                  ))}
                  {item.story_om && item.story_om !== item.story_en && (
                    <details className="mod-card-om">
                      <summary>View Afaan Oromo version</summary>
                      <div className="mod-card-om-text">
                        {item.story_om.split('\n').filter(p => p.trim()).map((para, i) => (
                          <p key={i}>{para}</p>
                        ))}
                      </div>
                    </details>
                  )}
                </div>

                <div className="mod-card-actions">
                  <button
                    className="mod-btn mod-btn-approve"
                    onClick={() => doAction(item.id, 'approve')}
                    disabled={!!actionLoading[item.id]}
                  >
                    {actionLoading[item.id] === 'approve' ? '…' : '✓ Approve & Publish'}
                  </button>
                  <button
                    className="mod-btn mod-btn-reject"
                    onClick={() => doAction(item.id, 'reject')}
                    disabled={!!actionLoading[item.id]}
                  >
                    {actionLoading[item.id] === 'reject' ? '…' : '✕ Reject'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
