/**
 * ============================================
 * Authentication Module
 * LinkedIn Branding Assistant
 * ============================================
 */

const API_BASE = 'http://localhost:5000/api';

// ── Token Management ────────────────────────

function getToken() {
    return localStorage.getItem('lb_token');
}

function setToken(token) {
    localStorage.setItem('lb_token', token);
}

function removeToken() {
    localStorage.removeItem('lb_token');
    localStorage.removeItem('lb_user');
}

function getUser() {
    const user = localStorage.getItem('lb_user');
    return user ? JSON.parse(user) : null;
}

function setUser(user) {
    localStorage.setItem('lb_user', JSON.stringify(user));
}

function isAuthenticated() {
    return !!getToken();
}

// ── Auth Guard ──────────────────────────────

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

function redirectIfAuth() {
    if (isAuthenticated()) {
        window.location.href = 'dashboard.html';
    }
}

// ── API Helper ──────────────────────────────

async function apiRequest(endpoint, method = 'GET', body = null) {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await response.json();

    if (response.status === 401) {
        removeToken();
        window.location.href = 'login.html';
        return null;
    }

    if (!response.ok) {
        throw new Error(data.error || 'Request failed');
    }

    return data;
}

// ── Register ────────────────────────────────

async function handleRegister(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;

    try {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
        btn.disabled = true;

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const careerGoal = document.getElementById('careerGoal')?.value?.trim() || '';

        if (password !== confirmPassword) {
            throw new Error('Passwords do not match');
        }

        const data = await apiRequest('/auth/register', 'POST', {
            name, email, password, career_goal: careerGoal
        });

        setToken(data.token);
        setUser(data.user);
        showToast('Account created successfully!', 'success');

        setTimeout(() => window.location.href = 'dashboard.html', 1000);
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// ── Login ───────────────────────────────────

async function handleLogin(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;

    try {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing In...';
        btn.disabled = true;

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        const data = await apiRequest('/auth/login', 'POST', { email, password });

        setToken(data.token);
        setUser(data.user);
        showToast('Welcome back!', 'success');

        setTimeout(() => window.location.href = 'dashboard.html', 1000);
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// ── Logout ──────────────────────────────────

function handleLogout() {
    removeToken();
    showToast('Logged out successfully', 'info');
    setTimeout(() => window.location.href = 'login.html', 500);
}

// ── Toast Notifications ─────────────────────

function showToast(message, type = 'info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const icons = { success: 'fa-check-circle', error: 'fa-exclamation-circle', info: 'fa-info-circle' };
    const toast = document.createElement('div');
    toast.className = `toast-custom ${type}`;
    toast.innerHTML = `<i class="fas ${icons[type] || icons.info}"></i><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ── Theme Toggle ────────────────────────────

function initTheme() {
    const saved = localStorage.getItem('lb_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('lb_theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const btn = document.getElementById('themeToggle');
    if (btn) {
        btn.innerHTML = theme === 'dark'
            ? '<i class="fas fa-sun"></i>'
            : '<i class="fas fa-moon"></i>';
    }
}

// ── Initialize ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initTheme();

    const loginForm = document.getElementById('loginForm');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);

    const registerForm = document.getElementById('registerForm');
    if (registerForm) registerForm.addEventListener('submit', handleRegister);

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);

    const themeBtn = document.getElementById('themeToggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Update user display
    const user = getUser();
    const nameEl = document.getElementById('userName');
    if (nameEl && user) nameEl.textContent = user.name;
});
