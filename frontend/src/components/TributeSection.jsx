import { useState, useEffect } from 'react';
import './TributeSection.css';

function FlameIcon({ lit = false, size = 28 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 28"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`flame-svg ${lit ? 'flame-lit' : ''}`}
      aria-hidden="true"
    >
      <path
        d="M12 2C12 2 7 8 7 13.5C7 16.538 9.239 19 12 19C14.761 19 17 16.538 17 13.5C17 10.5 15 8.5 15 8.5C15 8.5 14.5 11 13 11C13 8 12 2 12 2Z"
        fill={lit ? '#e8c268' : 'currentColor'}
        className="flame-body"
      />
      <path
        d="M12 19C12 19 10 17.5 10 15.5C10 14.119 10.895 13 12 13C13.105 13 14 14.119 14 15.5C14 17.5 12 19 12 19Z"
        fill={lit ? '#fff3d0' : 'currentColor'}
        className="flame-core"
        opacity={lit ? 0.9 : 0.5}
      />
      <rect x="11" y="19" width="2" height="7" rx="1" fill={lit ? '#c8a040' : 'currentColor'} opacity="0.6" className="flame-wick" />
    </svg>
  );
}

function formatDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

export default function TributeSection({ slug }) {
  const [candleCount, setCandleCount] = useState(0);
  const [messages, setMessages] = useState([]);
  const [messageCount, setMessageCount] = useState(0);
  const [loading, setLoading] = useState(true);

  const [mode, setMode] = useState('candle');
  const [authorName, setAuthorName] = useState('');
  const [messageText, setMessageText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [justLitCandle, setJustLitCandle] = useState(false);
  const [justSentMessage, setJustSentMessage] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`/api/legacies/${slug}/tributes/`)
      .then(r => r.json())
      .then(data => {
        setCandleCount(data.candle_count || 0);
        setMessages(data.messages || []);
        setMessageCount(data.message_count || 0);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [slug]);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    const body = {
      tribute_type: mode,
      author_name: authorName.trim(),
      message: mode === 'message' ? messageText.trim() : '',
    };

    try {
      const res = await fetch(`/api/legacies/${slug}/tributes/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.message?.[0] || 'Something went wrong. Please try again.');
        setSubmitting(false);
        return;
      }
      if (mode === 'candle') {
        setCandleCount(data.candle_count);
        setJustLitCandle(true);
        setTimeout(() => setJustLitCandle(false), 4000);
      } else {
        setMessages(prev => [data.tribute, ...prev]);
        setMessageCount(prev => prev + 1);
        setJustSentMessage(true);
        setTimeout(() => setJustSentMessage(false), 4000);
        setMessageText('');
      }
      setAuthorName('');
      setSubmitting(false);
    } catch {
      setError('Could not connect. Please try again.');
      setSubmitting(false);
    }
  }

  return (
    <section className="tribute-section" aria-label="Tributes">
      <div className="tribute-divider">
        <span className="tribute-divider-line" />
        <span className="tribute-divider-icon" aria-hidden="true">✦</span>
        <span className="tribute-divider-line" />
      </div>

      <h2 className="tribute-heading">Leave a Tribute</h2>
      <p className="tribute-subheading">
        Light a candle in their memory, or leave words that will remain with their story.
      </p>

      <div className="candle-count-bar">
        <FlameIcon lit={candleCount > 0 || justLitCandle} size={32} />
        <span className="candle-count-text">
          {candleCount === 0
            ? 'Be the first to light a candle'
            : candleCount === 1
            ? '1 candle has been lit'
            : `${candleCount} candles have been lit`}
        </span>
      </div>

      {justLitCandle && (
        <div className="tribute-success candle-success" role="status">
          <FlameIcon lit size={20} />
          <span>Your candle burns here. May their memory be light.</span>
        </div>
      )}

      {justSentMessage && (
        <div className="tribute-success message-success" role="status">
          <span>✦</span>
          <span>Your words have been received. They will remain here.</span>
        </div>
      )}

      <form className="tribute-form" onSubmit={handleSubmit}>
        <div className="tribute-mode-toggle" role="group" aria-label="Tribute type">
          <button
            type="button"
            className={`mode-btn ${mode === 'candle' ? 'active' : ''}`}
            onClick={() => { setMode('candle'); setError(''); }}
          >
            <FlameIcon lit={mode === 'candle'} size={18} />
            Light a Candle
          </button>
          <button
            type="button"
            className={`mode-btn ${mode === 'message' ? 'active' : ''}`}
            onClick={() => { setMode('message'); setError(''); }}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            Leave a Message
          </button>
        </div>

        <div className="tribute-fields">
          <input
            type="text"
            className="tribute-input"
            placeholder="Your name (optional — leave blank to be anonymous)"
            value={authorName}
            onChange={e => setAuthorName(e.target.value)}
            maxLength={100}
          />

          {mode === 'message' && (
            <textarea
              className="tribute-textarea"
              placeholder="Write your tribute… a memory, a prayer, a few words that carry their meaning forward."
              value={messageText}
              onChange={e => setMessageText(e.target.value)}
              rows={4}
              maxLength={1000}
              required
            />
          )}

          {error && <p className="tribute-error" role="alert">{error}</p>}

          <button
            type="submit"
            className={`tribute-submit ${mode}`}
            disabled={submitting}
          >
            {submitting
              ? 'Sending…'
              : mode === 'candle'
              ? 'Light the Candle'
              : 'Leave this Tribute'}
          </button>
        </div>
      </form>

      {!loading && messages.length > 0 && (
        <div className="message-wall">
          <h3 className="message-wall-heading">
            {messageCount === 1 ? '1 tribute left' : `${messageCount} tributes left`}
          </h3>
          <div className="message-list">
            {messages.map(m => (
              <div key={m.id} className="tribute-message-card">
                <div className="tribute-message-header">
                  <span className="tribute-author">
                    {m.author_name?.trim() || 'Anonymous'}
                  </span>
                  <span className="tribute-date">{formatDate(m.created_at)}</span>
                </div>
                <p className="tribute-message-text">{m.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {!loading && messages.length === 0 && (
        <p className="tribute-empty">
          No messages yet. Be the first to leave words for their memory.
        </p>
      )}
    </section>
  );
}
