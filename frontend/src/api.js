const BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, options);
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw { status: res.status, data };
  }
  return res.json();
}

export async function fetchLegacies({ q = '', zone = '', page = 1 } = {}) {
  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (zone) params.set('zone', zone);
  if (page > 1) params.set('page', page);
  const query = params.toString();
  return request(`/legacies/${query ? '?' + query : ''}`);
}

export async function fetchLegacy(slug) {
  return request(`/legacies/${slug}/`);
}

export async function fetchZones() {
  return request('/zones/');
}

export async function submitLegacy(formData) {
  const res = await fetch(`${BASE}/legacies/submit/`, {
    method: 'POST',
    body: formData,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw { status: res.status, data };
  return data;
}
