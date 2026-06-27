/**
 * ============================================
 * Dashboard Module
 * LinkedIn Branding Assistant
 * ============================================
 */

// ── Dashboard Init ──────────────────────────

async function initDashboard() {
    if (!requireAuth()) return;
    loadUserInfo();
    await loadDashboardStats();
    initSidebar();
}

function loadUserInfo() {
    const user = getUser();
    if (!user) return;
    const el = document.getElementById('userName');
    if (el) el.textContent = user.name || 'User';
    const emailEl = document.getElementById('userEmail');
    if (emailEl) emailEl.textContent = user.email || '';
}

async function loadDashboardStats() {
    try {
        const data = await apiRequest('/history/stats');
        if (!data) return;
        const s = data.stats;

        const updates = {
            'statPosts': s.posts_generated || 0,
            'statScore': s.branding_score || 0,
            'statHeadlines': s.headlines_generated || 0,
            'statCompletion': s.profile_completion || 0
        };

        Object.entries(updates).forEach(([id, val]) => {
            const el = document.getElementById(id);
            if (el) animateCounter(el, val);
        });

        // Update completion bar
        const bar = document.getElementById('completionBar');
        if (bar) bar.style.width = `${s.profile_completion || 0}%`;
    } catch (err) {
        console.error('Failed to load stats:', err);
    }
}

function animateCounter(el, target) {
    let current = 0;
    const increment = target / 40;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        el.textContent = Math.round(current);
    }, 30);
}

// ── Sidebar ─────────────────────────────────

function initSidebar() {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (toggle) {
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
        });
    }
    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }

    // Active link highlight
    const currentPage = window.location.pathname.split('/').pop() || 'dashboard.html';
    document.querySelectorAll('.sidebar-link').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

// ── History ─────────────────────────────────

async function loadHistory() {
    if (!requireAuth()) return;
    try {
        const data = await apiRequest('/history/');
        displayHistory(data.history || []);
    } catch (err) {
        showToast('Failed to load history', 'error');
    }
}

function displayHistory(history) {
    const container = document.getElementById('historyContainer');
    if (!container) return;

    if (!history.length) {
        container.innerHTML = `<div class="text-center py-5" style="color:var(--text-secondary)">
            <i class="fas fa-history" style="font-size:3rem;margin-bottom:1rem;opacity:0.3"></i>
            <p>No history yet. Start generating content!</p></div>`;
        return;
    }

    const typeIcons = {
        post: 'fa-file-alt', headline: 'fa-heading',
        about: 'fa-user-circle', branding_report: 'fa-chart-pie'
    };
    const typeColors = {
        post: 'var(--primary)', headline: 'var(--accent)',
        about: 'var(--success)', branding_report: 'var(--warning)'
    };

    container.innerHTML = history.map(item => {
        let preview = '';
        if (item.type === 'post') preview = item.content?.substring(0, 150) + '...';
        else if (item.type === 'headline') preview = (item.content || []).slice(0, 3).join(' • ');
        else if (item.type === 'about') preview = item.content?.substring(0, 150) + '...';
        else if (item.type === 'branding_report') preview = `Score: ${item.score}/100`;

        return `<div class="history-card glass-card fade-in" style="border-left-color:${typeColors[item.type] || 'var(--primary)'}">
            <div class="d-flex justify-content-between align-items-start">
                <div class="history-type" style="color:${typeColors[item.type]}">
                    <i class="fas ${typeIcons[item.type] || 'fa-file'} me-1"></i>${item.type.replace(/_/g, ' ')}
                </div>
                <button class="btn-glass" style="padding:4px 10px;font-size:0.75rem" onclick="deleteHistoryItem('${item.type}','${item.id}',this)">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="history-content">${preview}</div>
            <div class="history-date"><i class="fas fa-clock me-1"></i>${formatDate(item.created_at)}</div>
        </div>`;
    }).join('');
}

async function deleteHistoryItem(type, id, btn) {
    if (!confirm('Delete this item?')) return;
    try {
        await apiRequest(`/history/${type}/${id}`, 'DELETE');
        btn.closest('.history-card').remove();
        showToast('Item deleted', 'success');
    } catch (err) {
        showToast('Failed to delete', 'error');
    }
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

// ── Page Init ───────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const page = window.location.pathname.split('/').pop();

    if (['dashboard.html', 'profile-analysis.html', 'headline-generator.html',
         'about-generator.html', 'post-generator.html', 'hashtag-generator.html',
         'branding-score.html', 'history.html'].includes(page)) {
        if (!requireAuth()) return;
        initSidebar();
        loadUserInfo();
    }

    if (page === 'dashboard.html') loadDashboardStats();
    if (page === 'history.html') loadHistory();
});
