import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchZones, submitLegacy } from '../api';
import './SubmitLegacy.css';

export default function SubmitLegacy() {
  const [zones, setZones] = useState([]);
  const [form, setForm] = useState({ full_name: '', zone: '', story: '', photo: null });
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
    if (!form.full_name.trim()) errs.full_name = 'Full name is required.';
    if (!form.zone) errs.zone = 'Please select a zone.';
    if (!form.story.trim()) errs.story = 'Story is required.';
    if (form.story.trim().length < 30) errs.story = 'Story must be at least 30 characters.';
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
    fd.append('zone', form.zone);
    fd.append('story', form.story.trim());
    if (form.photo) fd.append('photo', form.photo);

    try {
      await submitLegacy(fd);
      setSuccess(true);
      setForm({ full_name: '', zone: '', story: '', photo: null });
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
            <div className="success-icon">✦</div>
            <h1>Thank You</h1>
            <p>
              Your submission has been received. It will be reviewed by a community
              moderator before it appears on the Legacy Wall. We honor your contribution
              to preserving this story.
            </p>
            <div className="success-actions">
              <Link to="/" className="btn btn-primary">View the Wall</Link>
              <button className="btn btn-outline" onClick={() => setSuccess(false)}>
                Submit Another
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="submit-page">
      <div className="container">
        <div className="submit-header">
          <h1 className="submit-title">Submit a Legacy</h1>
          <p className="submit-sub">
            Share the story of an Oromo individual to be preserved on the Legacy Wall.
            All submissions are reviewed by zone moderators before publication.
          </p>
        </div>

        {errors._general && (
          <div className="alert alert-error">{errors._general}</div>
        )}

        <form className="submit-form" onSubmit={handleSubmit} noValidate>
          <div className="form-section">
            <h2 className="form-section-title">Personal Information</h2>

            <div className="form-group">
              <label htmlFor="full_name" className="form-label">
                Full Name <span className="required">*</span>
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                className={`form-input ${errors.full_name ? 'input-error' : ''}`}
                placeholder="Enter the full name of the individual"
                value={form.full_name}
                onChange={handleChange}
              />
              {errors.full_name && <span className="form-error">{errors.full_name}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="zone" className="form-label">
                Zone (Oromiyaa Region) <span className="required">*</span>
              </label>
              <select
                id="zone"
                name="zone"
                className={`form-select ${errors.zone ? 'input-error' : ''}`}
                value={form.zone}
                onChange={handleChange}
              >
                <option value="">Select a zone…</option>
                {zones.map(z => (
                  <option key={z.id} value={z.id}>{z.name}</option>
                ))}
              </select>
              {errors.zone && <span className="form-error">{errors.zone}</span>}
              <span className="form-help">
                Select the zone of Oromiyaa this individual is from.
              </span>
            </div>
          </div>

          <div className="form-section">
            <h2 className="form-section-title">Their Story</h2>

            <div className="form-group">
              <label htmlFor="story" className="form-label">
                Biography / Story <span className="required">*</span>
              </label>
              <textarea
                id="story"
                name="story"
                className={`form-textarea ${errors.story ? 'input-error' : ''}`}
                placeholder="Share their life story, achievements, memories, and the impact they had on family and community…"
                value={form.story}
                onChange={handleChange}
                rows={10}
              />
              {errors.story && <span className="form-error">{errors.story}</span>}
              <span className="form-help">
                {form.story.length} characters — share as much as you'd like to preserve.
              </span>
            </div>
          </div>

          <div className="form-section">
            <h2 className="form-section-title">Photo <span className="optional">(Optional)</span></h2>

            <div className="form-group">
              <label htmlFor="photo" className="form-label">Upload a Photo</label>

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
                    ✕ Remove
                  </button>
                </div>
              )}

              <label htmlFor="photo" className="file-upload-label">
                <span className="file-icon">📷</span>
                <span>{form.photo ? form.photo.name : 'Click to choose a photo…'}</span>
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
              <span className="form-help">JPG, PNG, or WEBP. Max 10MB recommended.</span>
            </div>
          </div>

          <div className="submit-actions">
            <button type="submit" className="btn btn-primary btn-submit" disabled={submitting}>
              {submitting ? 'Submitting…' : 'Submit Legacy for Review'}
            </button>
            <Link to="/" className="btn btn-ghost">Cancel</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
