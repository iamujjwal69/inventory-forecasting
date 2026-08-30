const API_BASE = '/api';

async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/index.html';
        throw new Error('No token');
    }
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
    };
    const res = await fetch(url, { ...options, headers });
    if (res.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/index.html';
        throw new Error('Unauthorized');
    }
    if (!res.ok) {
        let err;
        try { err = await res.json(); } catch(e) { err = {}; }
        throw new Error(err.detail || 'API Error');
    }
    return res;
}

async function getProducts() {
    const res = await fetchWithAuth(`${API_BASE}/products`);
    return res.json();
}

async function getForecast(productId, days = 30) {
    const res = await fetchWithAuth(`${API_BASE}/forecast/${productId}?days=${days}`);
    return res.json();
}
