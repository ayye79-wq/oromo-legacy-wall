import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchZones, submitLegacy } from '../api';
import { useLang } from '../i18n/LanguageContext';
import './SubmitLegacy.css';

export default function SubmitLegacy() {
  const { t } = useLang();
  const [zones, setZones] = useState([]);
  const [storyLang, setStoryLang] = useState('en');
  const [form, setForm] = useState({
    full_name: '', occupation: '', zone: '',
    story_en: '', story_om: '', photo: null,
  });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);

  useEffect(() => {
    fetchZones()
      .then(data => setZones(Array.isArray(data) ? data : data.results || []))
      .catch(() => {});
  }, []);

  function handleChange(e) {
    const { name, value, files } = e.target;
    if (name === 'photo') {
      const file = files[0] || null;
      setForm(f => ({ ...f, photo: file }));
      if (file) {
        const reader = new FileReader();
        reader.onload = ev => setPreviewUrl(ev.target.result);
        reader.readAsDataURL(file);
      } else {
        setPreviewUrl(null);
      }
    } else {
      setForm(f => ({ ...f, [name]: value }));
      if (errors[name]) setErrors(e => ({ ...e, [name]: null }));
    }
  }

  function validate() {
    const errs = {};
    if (!form.full_name.trim()) errs.full_name = t('submit.full_name_required');
    if (!form.zone) errs.zone = t('submit.zone_required');

    const hasEn = form.story_en.trim().length > 0;
    const hasOm = form.story_om.trim().length > 0;

    if (!hasEn && !hasOm) {
      if (storyLang === 'om') errs.story_om = t('submit.story_required');
      else errs.story_en = t('submit.story_required');
    } else {
      if (hasEn && form.story_en.trim().length < 30) errs.story_en = t('submit.story_short');
      if (hasOm && form.story_om.trim().length < 30) errs.story_om = t('submit.story_short');
    }
    return errs;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }

    setSubmitting(true);
    setErrors({});

    const fd = new FormData();
    fd.append('full_name', form.full_name.trim());
    if (form.occupation.trim()) fd.append('occupation', form.occupation.trim());
    fd.append('zone', form.zone);
    if (form.story_en.trim()) fd.append('story_en', form.story_en.trim());
    if (form.story_om.trim()) fd.append('story_om', form.story_om.trim());
    fd.append('original_language', storyLang === 'both' ? 'en' : storyLang);
    const primaryStory = form.story_en.trim() || form.story_om.trim();
    fd.append('story', primaryStory);
    if (form.photo) fd.append('photo', form.photo);

    try {
      await submitLegacy(fd);
      setSuccess(true);
      setForm({ full_name: '', occupation: '', zone: '', story_en: '', story_om: '', photo: null });
      setPreviewUrl(null);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      if (err.data) {
        const apiErrs = {};
        Object.entries(err.data).forEach(([k, v]) => {
          apiErrs[k] = Array.isArray(v) ? v.join(' ') : String(v);
        });
        setErrors(apiErrs);
      } else {
        setErrors({ _general: t('submit.error_general') });
      }
    }

    setSubmitting(false);
  }

  if (success) {
    return (
      <div className="submit-page">
        <div className="container">
          <div className="success-card">
            <div className="success-candle" aria-hidden="true">🕯</div>
            <h1>{t('submit.success_title')}</h1>
            <div className="success-ornament">
              <span className="ornament-line-short" />
              <span style={{ color: 'var(--accent)', fontSize: '0.7rem' }}>✦</span>
              <span className="ornament-line-short" />
            </div>
            <p>{t('submit.success_body')}</p>
            <div className="success-actions">
              <Link to="/" className="btn btn-primary">{t('submit.success_return')}</Link>
              <button className="btn btn-outline" onClick={() => setSuccess(false)}>
                {t('submit.success_another')}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const showEn = storyLang === 'en' || storyLang === 'both';
  const showOm = storyLang === 'om' || storyLang === 'both';

  return (
    <div className="submit-page">
      <div className="submit-page-header">
        <div className="container">
          <p className="submit-kicker">{t('submit.kicker')}</p>
          <h1 className="submit-title">{t('submit.title')}</h1>
          <p className="submit-sub">{t('submit.subtitle')}</p>
        </div>
      </div>

      <div className="container submit-body">
        {errors._general && (
          <div className="alert alert-error">{errors._general}</div>
        )}

        <form className="submit-form" onSubmit={handleSubmit} noValidate>
          <div className="form-section">
            <h2 className="form-section-title">{t('submit.section_who')}</h2>

            <div className="form-group">
              <label htmlFor="full_name" className="form-label">
                {t('submit.full_name')} <span className="required">*</span>
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                className={`form-input ${errors.full_name ? 'input-error' : ''}`}
                placeholder={t('submit.full_name_placeholder')}
                value={form.full_name}
                onChange={handleChange}
              />
              {errors.full_name && <span className="form-error">{errors.full_name}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="occupation" className="form-label">
                {t('submit.occupation')} <span className="optional-label">{t('submit.occupation_optional')}</span>
              </label>
              <input
                id="occupation"
                name="occupation"
                type="text"
                className="form-input"
                placeholder={t('submit.occupation_placeholder')}
                value={form.occupation}
                onChange={handleChange}
              />
              <span className="form-help">{t('submit.occupation_help')}</span>
            </div>

            <div className="form-group">
              <label htmlFor="zone" className="form-label">
                {t('submit.zone')} <span className="required">*</span>
              </label>
              <select
                id="zone"
                name="zone"
                className={`form-select ${errors.zone ? 'input-error' : ''}`}
                value={form.zone}
                onChange={handleChange}
              >
                <option value="">{t('submit.zone_select')}</option>
                {zones.map(z => (
                  <option key={z.id} value={z.id}>{z.name}</option>
                ))}
              </select>
              {errors.zone && <span className="form-error">{errors.zone}</span>}
              <span className="form-help">{t('submit.zone_help')}</span>
            </div>
          </div>

          <div className="form-section">
            <h2 className="form-section-title">{t('submit.section_story')}</h2>
            <p className="section-note">{t('submit.story_note')}</p>

            <div className="form-group">
              <label className="form-label">{t('submit.story_lang')}</label>
              <div className="story-lang-toggle" role="group">
                {['en', 'om', 'both'].map(opt => (
                  <button
                    key={opt}
                    type="button"
                    className={`story-lang-btn ${storyLang === opt ? 'active' : ''}`}
                    onClick={() => setStoryLang(opt)}
                  >
                    {t(`submit.lang_${opt}`)}
                  </button>
                ))}
              </div>
            </div>

            {showEn && (
              <div className="form-group">
                <label htmlFor="story_en" className="form-label">
                  {storyLang === 'both' ? t('submit.story_en') : t('submit.section_story')}
                  {storyLang !== 'both' && <span className="required"> *</span>}
                </label>
                <textarea
                  id="story_en"
                  name="story_en"
                  className={`form-textarea ${errors.story_en ? 'input-error' : ''}`}
                  placeholder={t('submit.story_placeholder_en')}
                  value={form.story_en}
                  onChange={handleChange}
                  rows={10}
                />
                {errors.story_en && <span className="form-error">{errors.story_en}</span>}
                <span className="form-help">
                  {form.story_en.length > 0
                    ? t('submit.story_chars', { n: form.story_en.length })
                    : t('submit.story_no_min')}
                </span>
              </div>
            )}

            {showOm && (
              <div className="form-group">
                <label htmlFor="story_om" className="form-label">
                  {storyLang === 'both' ? t('submit.story_om') : t('submit.section_story')}
                  {storyLang !== 'both' && <span className="required"> *</span>}
                </label>
                <textarea
                  id="story_om"
                  name="story_om"
                  className={`form-textarea ${errors.story_om ? 'input-error' : ''}`}
                  placeholder={t('submit.story_placeholder_om')}
                  value={form.story_om}
                  onChange={handleChange}
                  rows={10}
                  dir="ltr"
                />
                {errors.story_om && <span className="form-error">{errors.story_om}</span>}
                <span className="form-help">
                  {form.story_om.length > 0
                    ? t('submit.story_chars', { n: form.story_om.length })
                    : t('submit.story_no_min')}
                </span>
              </div>
            )}
          </div>

          <div className="form-section">
            <h2 className="form-section-title">
              {t('submit.section_photo')} <span className="optional-label">{t('submit.occupation_optional')}</span>
            </h2>
            <p className="section-note">{t('submit.photo_note')}</p>

            <div className="form-group" style={{ marginBottom: 0 }}>
              {previewUrl && (
                <div className="photo-preview">
                  <img src={previewUrl} alt="Preview" />
                  <button
                    type="button"
                    className="photo-remove"
                    onClick={() => {
                      setForm(f => ({ ...f, photo: null }));
                      setPreviewUrl(null);
                    }}
                  >
                    {t('submit.photo_remove')}
                  </button>
                </div>
              )}

              <label htmlFor="photo" className="file-upload-label">
                <span>🕯</span>
                <span>{form.photo ? form.photo.name : t('submit.photo_choose')}</span>
                <input
                  id="photo"
                  name="photo"
                  type="file"
                  accept="image/*"
                  onChange={handleChange}
                  className="file-input-hidden"
                />
              </label>
              {errors.photo && <span className="form-error">{errors.photo}</span>}
              <span className="form-help">{t('submit.photo_help')}</span>
            </div>
          </div>

          <div className="submit-actions">
            <button type="submit" className="btn btn-primary btn-submit" disabled={submitting}>
              {submitting ? t('submit.btn_submitting') : t('submit.btn')}
            </button>
            <Link to="/" className="btn btn-ghost">{t('submit.btn_return')}</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
