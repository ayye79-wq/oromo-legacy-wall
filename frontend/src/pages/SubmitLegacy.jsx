import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchZones, submitLegacy } from '../api';
import './SubmitLegacy.css';

export default function SubmitLegacy() {
  const [zones, setZones] = useState([]);
  const [form, setForm] = useState({ full_name: '', occupation: '', zone: '', story: '', photo: null });
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
    if (!form.full_name.trim()) errs.full_name = 'Their full name is required.';
    if (!form.zone) errs.zone = 'Please select the zone they are from.';
    if (!form.story.trim()) errs.story = 'Please share their story.';
    if (form.story.trim().length < 30) errs.story = 'Please share a little more — at least 30 characters.';
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
    fd.append('story', form.story.trim());
    if (form.photo) fd.append('photo', form.photo);

    try {
      await submitLegacy(fd);
      setSuccess(true);
      setForm({ full_name: '', occupation: '', zone: '', story: '', photo: null });
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
        setErrors({ _general: 'Something went wrong. Please try again.' });
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
            <h1>Their Story Has Been Received</h1>
            <div className="success-ornament">
              <span className="ornament-line-short" />
              <span style={{ color: 'var(--accent)', fontSize: '0.7rem' }}>✦</span>
              <span className="ornament-line-short" />
            </div>
            <p>
              Your tribute has been received with honor. A community moderator
              will review it carefully before it is placed on the Memorial Wall.
              Thank you for helping preserve this life for generations to come.
            </p>
            <div className="success-actions">
              <Link to="/" className="btn btn-primary">Return to the Wall</Link>
              <button className="btn btn-outline" onClick={() => setSuccess(false)}>
                Honor Another Life
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="submit-page">
      <div className="submit-page-header">
        <div className="container">
          <p className="submit-kicker">In Their Memory</p>
          <h1 className="submit-title">Honor a Life</h1>
          <p className="submit-sub">
            Share the story of an Oromo individual so that their life may be preserved
            on this wall. Every submission is reviewed by a trusted community moderator
            before it is placed here.
          </p>
        </div>
      </div>

      <div className="container submit-body">
        {errors._general && (
          <div className="alert alert-error">{errors._general}</div>
        )}

        <form className="submit-form" onSubmit={handleSubmit} noValidate>
          <div className="form-section">
            <h2 className="form-section-title">Who Are You Honoring?</h2>

            <div className="form-group">
              <label htmlFor="full_name" className="form-label">
                Full Name <span className="required">*</span>
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                className={`form-input ${errors.full_name ? 'input-error' : ''}`}
                placeholder="Their full name…"
                value={form.full_name}
                onChange={handleChange}
              />
              {errors.full_name && <span className="form-error">{errors.full_name}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="occupation" className="form-label">
                Their Role or Calling <span className="optional-label">(optional)</span>
              </label>
              <input
                id="occupation"
                name="occupation"
                type="text"
                className="form-input"
                placeholder="e.g. Teacher, farmer, mother of seven, community elder…"
                value={form.occupation}
                onChange={handleChange}
              />
              <span className="form-help">One line that captures who they were. This appears on their memorial card.</span>
            </div>

            <div className="form-group">
              <label htmlFor="zone" className="form-label">
                Zone of Oromiyaa <span className="required">*</span>
              </label>
              <select
                id="zone"
                name="zone"
                className={`form-select ${errors.zone ? 'input-error' : ''}`}
                value={form.zone}
                onChange={handleChange}
              >
                <option value="">Select their zone…</option>
                {zones.map(z => (
                  <option key={z.id} value={z.id}>{z.name}</option>
                ))}
              </select>
              {errors.zone && <span className="form-error">{errors.zone}</span>}
              <span className="form-help">Which zone of Oromiyaa were they from?</span>
            </div>
          </div>

          <div className="form-section">
            <h2 className="form-section-title">Their Story</h2>
            <p className="section-note">
              Write as much as you'd like. Share who they were, what they meant to
              you, their life, their contributions, their legacy.
            </p>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label htmlFor="story" className="form-label">
                Biography &amp; Story <span className="required">*</span>
              </label>
              <textarea
                id="story"
                name="story"
                className={`form-textarea ${errors.story ? 'input-error' : ''}`}
                placeholder="In the words of those who loved them…"
                value={form.story}
                onChange={handleChange}
                rows={12}
              />
              {errors.story && <span className="form-error">{errors.story}</span>}
              <span className="form-help">
                {form.story.length > 0 ? `${form.story.length} characters written` : 'No minimum length — share what feels right.'}
              </span>
            </div>
          </div>

          <div className="form-section">
            <h2 className="form-section-title">
              A Photo <span className="optional-label">(optional)</span>
            </h2>
            <p className="section-note">
              A photograph helps bring their memory to life on the wall.
            </p>

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
                    Remove
                  </button>
                </div>
              )}

              <label htmlFor="photo" className="file-upload-label">
                <span>🕯</span>
                <span>{form.photo ? form.photo.name : 'Choose a photograph…'}</span>
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
              <span className="form-help">JPG, PNG, or WEBP — any size is welcome.</span>
            </div>
          </div>

          <div className="submit-actions">
            <button type="submit" className="btn btn-primary btn-submit" disabled={submitting}>
              {submitting ? 'Preserving their memory…' : 'Place Their Story on the Wall'}
            </button>
            <Link to="/" className="btn btn-ghost">Return to the Wall</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
