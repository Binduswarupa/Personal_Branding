/**
 * ============================================
 * AI Module - Groq API Integration
 * LinkedIn Branding Assistant
 * ============================================
 */

// ── Spinner Control ─────────────────────────

function showSpinner(message = 'AI is thinking...') {
    let overlay = document.getElementById('spinnerOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'spinnerOverlay';
        overlay.className = 'spinner-overlay';
        overlay.innerHTML = `
            <div style="text-align:center">
                <div class="ai-spinner"></div>
                <p class="ai-spinner-text" id="spinnerText">${message}</p>
            </div>`;
        document.body.appendChild(overlay);
    }
    const txt = document.getElementById('spinnerText');
    if (txt) txt.textContent = message;
    overlay.classList.add('active');
}

function hideSpinner() {
    const overlay = document.getElementById('spinnerOverlay');
    if (overlay) overlay.classList.remove('active');
}

// ── Profile Analysis ────────────────────────

async function analyzeProfile() {
    try {
        showSpinner('Analyzing your LinkedIn profile...');
        const data = {
            headline: document.getElementById('headline')?.value || '',
            about: document.getElementById('about')?.value || '',
            skills: document.getElementById('skills')?.value || '',
            experience: document.getElementById('experience')?.value || '',
            projects: document.getElementById('projects')?.value || '',
            education: document.getElementById('education')?.value || ''
        };

        const result = await apiRequest('/profile/analyze', 'POST', data);
        displayProfileAnalysis(result.analysis);
        showToast('Profile analysis complete!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        hideSpinner();
    }
}

function displayProfileAnalysis(analysis) {
    const container = document.getElementById('analysisResult');
    if (!container) return;

    const bd = analysis.breakdown || {};
    container.innerHTML = `
        <div class="fade-in">
            <div class="row g-3 mb-4">
                <div class="col-12 text-center">
                    <div class="progress-circle" style="margin:0 auto">
                        <svg width="160" height="160">
                            <defs><linearGradient id="gradient" x1="0%" y1="0%" x2="100%"><stop offset="0%" style="stop-color:#0A66C2"/><stop offset="100%" style="stop-color:#38BDF8"/></linearGradient></defs>
                            <circle class="progress-bg" cx="80" cy="80" r="70"/>
                            <circle class="progress-bar" cx="80" cy="80" r="70" stroke-dasharray="440" stroke-dashoffset="${440 - (440 * (analysis.overall_score || 0) / 100)}"/>
                        </svg>
                        <div class="progress-text">
                            <div class="progress-value">${analysis.overall_score || 0}</div>
                            <div class="progress-label">Overall Score</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row g-3 mb-4">
                ${Object.entries(bd).map(([key, val]) => `
                    <div class="col-md-4 col-6">
                        <div class="glass-card text-center p-3">
                            <div style="font-size:1.5rem;font-weight:800;color:var(--primary)">${val}</div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);text-transform:capitalize">${key.replace(/_/g, ' ')}</div>
                        </div>
                    </div>
                `).join('')}
            </div>
            ${analysis.strengths?.length ? `
                <div class="glass-card mb-3">
                    <h6><i class="fas fa-check-circle text-success me-2"></i>Strengths</h6>
                    <ul class="mt-2">${analysis.strengths.map(s => `<li style="margin-bottom:4px;color:var(--text-secondary)">${s}</li>`).join('')}</ul>
                </div>` : ''}
            ${analysis.suggestions?.length ? `
                <div class="glass-card mb-3">
                    <h6><i class="fas fa-lightbulb text-warning me-2"></i>Suggestions</h6>
                    <ul class="mt-2">${analysis.suggestions.map(s => `<li style="margin-bottom:4px;color:var(--text-secondary)">${s}</li>`).join('')}</ul>
                </div>` : ''}
            ${analysis.improvement_roadmap?.length ? `
                <div class="glass-card mb-3">
                    <h6><i class="fas fa-road me-2"></i>Improvement Roadmap</h6>
                    ${analysis.improvement_roadmap.map(r => `
                        <div class="d-flex gap-2 align-items-start mt-2">
                            <span class="badge-custom ${r.priority === 'high' ? 'badge-primary' : r.priority === 'medium' ? 'badge-warning' : 'badge-success'}">${r.priority}</span>
                            <div><strong>${r.action}</strong><br><small style="color:var(--text-secondary)">${r.impact}</small></div>
                        </div>
                    `).join('')}
                </div>` : ''}
        </div>`;
}

// ── Headline Generation ─────────────────────

async function generateHeadlines() {
    try {
        showSpinner('Crafting recruiter-friendly headlines...');
        const data = {
            skills: document.getElementById('hlSkills')?.value || '',
            experience: document.getElementById('hlExperience')?.value || '',
            career_goal: document.getElementById('hlCareerGoal')?.value || ''
        };
        const result = await apiRequest('/content/generate-headlines', 'POST', data);
        displayHeadlines(result.result);
        showToast('Headlines generated!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        hideSpinner();
    }
}

function displayHeadlines(result) {
    const container = document.getElementById('headlinesResult');
    if (!container) return;
    const headlines = result.headlines || [];
    container.innerHTML = `
        <div class="fade-in">
            ${headlines.map((h, i) => `
                <div class="headline-card glass-card">
                    <div class="headline-text"><span class="badge-custom badge-primary me-2">${i + 1}</span>${h}</div>
                    <div class="headline-actions">
                        <button class="btn-glass" onclick="copyText('${h.replace(/'/g, "\\'")}')"><i class="fas fa-copy"></i></button>
                    </div>
                </div>
            `).join('')}
            ${result.tips?.length ? `
                <div class="glass-card mt-3">
                    <h6><i class="fas fa-lightbulb text-warning me-2"></i>Pro Tips</h6>
                    <ul class="mt-2">${result.tips.map(t => `<li style="color:var(--text-secondary)">${t}</li>`).join('')}</ul>
                </div>` : ''}
        </div>`;
}

// ── About Section Generation ────────────────

async function generateAbout() {
    try {
        showSpinner('Writing your professional summary...');
        const data = {
            skills: document.getElementById('abSkills')?.value || '',
            education: document.getElementById('abEducation')?.value || '',
            career_goals: document.getElementById('abCareerGoals')?.value || '',
            projects: document.getElementById('abProjects')?.value || '',
            experience: document.getElementById('abExperience')?.value || '',
            tone: document.getElementById('abTone')?.value || 'professional'
        };
        const result = await apiRequest('/content/generate-about', 'POST', data);
        displayAbout(result.result);
        showToast('About section generated!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        hideSpinner();
    }
}

function displayAbout(result) {
    const container = document.getElementById('aboutResult');
    if (!container) return;
    container.innerHTML = `
        <div class="fade-in">
            <div class="output-area">${result.about_section || ''}</div>
            <div class="output-actions">
                <button class="btn-primary-custom" onclick="copyText(document.querySelector('.output-area').textContent)">
                    <i class="fas fa-copy"></i> Copy
                </button>
            </div>
            ${result.ats_keywords_used?.length ? `
                <div class="mt-3">
                    <h6 class="mb-2">ATS Keywords Used</h6>
                    <div class="d-flex flex-wrap gap-2">
                        ${result.ats_keywords_used.map(k => `<span class="tag-chip">${k}</span>`).join('')}
                    </div>
                </div>` : ''}
        </div>`;
}

// ── Post Generation ─────────────────────────

let selectedCategory = 'Career Growth';
let selectedLength = 'medium';

function selectCategory(el, category) {
    document.querySelectorAll('.category-card').forEach(c => c.classList.remove('selected'));
    el.classList.add('selected');
    selectedCategory = category;
}

function selectLength(el, length) {
    document.querySelectorAll('.length-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    selectedLength = length;
}

async function generatePost() {
    try {
        showSpinner('Creating your LinkedIn post...');
        const data = {
            category: selectedCategory,
            post_length: selectedLength,
            topic: document.getElementById('postTopic')?.value || '',
            tone: document.getElementById('postTone')?.value || 'professional'
        };
        const result = await apiRequest('/content/generate-post', 'POST', data);
        displayPost(result.result);
        showToast('Post generated!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        hideSpinner();
    }
}

function displayPost(result) {
    const container = document.getElementById('postResult');
    if (!container) return;
    container.innerHTML = `
        <div class="fade-in">
            <div class="output-area" id="postContent">${(result.post_content || '').replace(/\n/g, '<br>')}</div>
            <div class="output-actions">
                <button class="btn-primary-custom" onclick="copyText(document.getElementById('postContent').innerText)">
                    <i class="fas fa-copy"></i> Copy Post
                </button>
            </div>
            ${result.emoji_suggestions?.length ? `
                <div class="mt-3">
                    <h6>Suggested Emojis</h6>
                    <div class="d-flex flex-wrap gap-2 mt-1">
                        ${result.emoji_suggestions.map(e => `<span class="tag-chip" onclick="copyText('${e}')">${e}</span>`).join('')}
                    </div>
                </div>` : ''}
            ${result.cta_suggestions?.length ? `
                <div class="mt-3">
                    <h6>Call-to-Action Ideas</h6>
                    <ul>${result.cta_suggestions.map(c => `<li style="color:var(--text-secondary)">${c}</li>`).join('')}</ul>
                </div>` : ''}
        </div>`;
}

// ── Hashtag Generation ──────────────────────

async function generateHashtags() {
    try {
        showSpinner('Finding trending hashtags...');
        const data = {
            topic: document.getElementById('hashTopic')?.value || '',
            industry: document.getElementById('hashIndustry')?.value || '',
            target_audience: document.getElementById('hashAudience')?.value || ''
        };
        const result = await apiRequest('/content/generate-hashtags', 'POST', data);
        displayHashtags(result.result);
        showToast('Hashtags generated!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        hideSpinner();
    }
}

function displayHashtags(result) {
    const container = document.getElementById('hashtagsResult');
    if (!container) return;
    const sections = [
        { title: '🔥 Trending', tags: result.trending_hashtags },
        { title: '🎯 Niche', tags: result.niche_hashtags },
        { title: '🚀 High Reach', tags: result.high_reach_hashtags },
        { title: '✨ Recommended Combo', tags: result.recommended_combination }
    ];
    container.innerHTML = `<div class="fade-in">
        ${sections.filter(s => s.tags?.length).map(s => `
            <div class="mb-3">
                <h6>${s.title}</h6>
                <div class="d-flex flex-wrap gap-2 mt-1">
                    ${s.tags.map(t => `<span class="tag-chip" onclick="copyText('${t}')">${t}</span>`).join('')}
                </div>
            </div>
        `).join('')}
        <button class="btn-primary-custom mt-2" onclick="copyAllHashtags()">
            <i class="fas fa-copy"></i> Copy All
        </button>
    </div>`;
    window._allHashtags = [...(result.trending_hashtags || []), ...(result.niche_hashtags || []), ...(result.high_reach_hashtags || [])];
}

function copyAllHashtags() {
    if (window._allHashtags) copyText(window._allHashtags.join(' '));
}

// ── Branding Score ──────────────────────────

async function calculateBrandingScore() {
    try {
        showSpinner('Calculating your branding score...');
        const data = {
            headline: document.getElementById('bsHeadline')?.value || '',
            about: document.getElementById('bsAbout')?.value || '',
            skills: document.getElementById('bsSkills')?.value || '',
            experience: document.getElementById('bsExperience')?.value || '',
            projects: document.getElementById('bsProjects')?.value || '',
            education: document.getElementById('bsEducation')?.value || ''
        };
        const result = await apiRequest('/branding/score', 'POST', data);
        displayBrandingScore(result.result);
        showToast('Branding score calculated!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        hideSpinner();
    }
}

function displayBrandingScore(result) {
    const container = document.getElementById('brandingResult');
    if (!container) return;

    const cats = result.categories || {};
    container.innerHTML = `
        <div class="fade-in">
            <div class="text-center mb-4">
                <div class="progress-circle">
                    <svg width="160" height="160">
                        <defs><linearGradient id="gradient" x1="0%" y1="0%" x2="100%"><stop offset="0%" style="stop-color:#0A66C2"/><stop offset="100%" style="stop-color:#38BDF8"/></linearGradient></defs>
                        <circle class="progress-bg" cx="80" cy="80" r="70"/>
                        <circle class="progress-bar" cx="80" cy="80" r="70" stroke-dasharray="440" stroke-dashoffset="${440 - (440 * (result.overall_score || 0) / 100)}"/>
                    </svg>
                    <div class="progress-text">
                        <div class="progress-value">${result.overall_score || 0}</div>
                        <div class="progress-label">Branding Score</div>
                    </div>
                </div>
            </div>
            <div class="chart-container mb-4"><canvas id="radarChart"></canvas></div>
            <div class="row g-3 mb-4">
                ${Object.entries(cats).map(([key, val]) => `
                    <div class="col-md-6">
                        <div class="glass-card p-3">
                            <div class="d-flex justify-content-between mb-1">
                                <span style="text-transform:capitalize;font-weight:600">${key.replace(/_/g, ' ')}</span>
                                <span style="font-weight:700;color:var(--primary)">${val.score || 0}</span>
                            </div>
                            <div style="height:6px;background:var(--border);border-radius:3px;overflow:hidden">
                                <div style="width:${val.score || 0}%;height:100%;background:linear-gradient(90deg,var(--primary),var(--accent));border-radius:3px;transition:width 1s ease"></div>
                            </div>
                            <small style="color:var(--text-secondary)">${val.details || ''}</small>
                        </div>
                    </div>
                `).join('')}
            </div>
            ${result.recommendations?.length ? `
                <div class="glass-card mb-3"><h6><i class="fas fa-star text-warning me-2"></i>Recommendations</h6>
                <ul class="mt-2">${result.recommendations.map(r => `<li style="color:var(--text-secondary)">${r}</li>`).join('')}</ul></div>` : ''}
            ${result.quick_wins?.length ? `
                <div class="glass-card"><h6><i class="fas fa-bolt text-success me-2"></i>Quick Wins</h6>
                <ul class="mt-2">${result.quick_wins.map(q => `<li style="color:var(--text-secondary)">${q}</li>`).join('')}</ul></div>` : ''}
        </div>`;

    // Render radar chart
    if (typeof initRadarChart === 'function') {
        const labels = Object.keys(cats).map(k => k.replace(/_/g, ' '));
        const values = Object.values(cats).map(v => v.score || 0);
        initRadarChart(labels, values);
    }
}

// ── Utility ─────────────────────────────────

function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        // Fallback
        const ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta);
        ta.select(); document.execCommand('copy');
        document.body.removeChild(ta);
        showToast('Copied to clipboard!', 'success');
    });
}
