import { useState, useEffect } from 'react';
import { useLang } from '../i18n/LanguageContext';
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
  const { t } = useLang();
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
        setError(data.message?.[0] || t('tribute.error_connect'));
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
      setError(t('tribute.error_connect'));
      setSubmitting(false);
    }
  }

  function candleLabel() {
    if (candleCount === 0) return t('tribute.candle_zero');
    if (candleCount === 1) return t('tribute.candle_one');
    return t('tribute.candle_many', { n: candleCount });
  }

  function messageCountLabel() {
    if (messageCount === 1) return t('tribute.count_one');
    return t('tribute.count_many', { n: messageCount });
  }

  return (
    <section className="tribute-section" aria-label="Tributes">
      <div className="tribute-divider">
        <span className="tribute-divider-line" />
        <span className="tribute-divider-icon" aria-hidden="true">✦</span>
        <span className="tribute-divider-line" />
      </div>

      <h2 className="tribute-heading">{t('tribute.heading')}</h2>
      <p className="tribute-subheading">{t('tribute.subheading')}</p>

      <div className="candle-count-bar">
        <FlameIcon lit={candleCount > 0 || justLitCandle} size={32} />
        <span className="candle-count-text">{candleLabel()}</span>
      </div>

      {justLitCandle && (
        <div className="tribute-success candle-success" role="status">
          <FlameIcon lit size={20} />
          <span>{t('tribute.success_candle')}</span>
        </div>
      )}

      {justSentMessage && (
        <div className="tribute-success message-success" role="status">
          <span>✦</span>
          <span>{t('tribute.success_message')}</span>
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
            {t('tribute.mode_candle')}
          </button>
          <button
            type="button"
            className={`mode-btn ${mode === 'message' ? 'active' : ''}`}
            onClick={() => { setMode('message'); setError(''); }}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            {t('tribute.mode_message')}
          </button>
        </div>

        <div className="tribute-fields">
          <input
            type="text"
            className="tribute-input"
            placeholder={t('tribute.name_placeholder')}
            value={authorName}
            onChange={e => setAuthorName(e.target.value)}
            maxLength={100}
          />

          {mode === 'message' && (
            <textarea
              className="tribute-textarea"
              placeholder={t('tribute.message_placeholder')}
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
              ? t('tribute.submitting')
              : mode === 'candle'
              ? t('tribute.submit_candle')
              : t('tribute.submit_message')}
          </button>
        </div>
      </form>

      {!loading && messages.length > 0 && (
        <div className="message-wall">
          <h3 className="message-wall-heading">{messageCountLabel()}</h3>
          <div className="message-list">
            {messages.map(m => (
              <div key={m.id} className="tribute-message-card">
                <div className="tribute-message-header">
                  <span className="tribute-author">
                    {m.author_name?.trim() || t('tribute.anonymous')}
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
        <p className="tribute-empty">{t('tribute.empty')}</p>
      )}
    </section>
  );
}
